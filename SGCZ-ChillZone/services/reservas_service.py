from datetime import datetime, time, timedelta, date
from datetime import timedelta as dt_timedelta
from flask import session
from typing import Tuple, Dict, List
import repositories.reserva_repository as reserva_repo
import repositories.recurso_repository as recurso_repo
import repositories.config_repository as conf_repo
import repositories.uso_repository as uso_repo
import repositories.user_repository as user_repo
from utils.validators import parse_time_str, validate_slot, time_overlap


def _extraer_valor_config(item, default: str) -> str:
    """Soporta distintos formatos de mocks: dict con 'valor', lista de dicts, o string directo."""
    if not item:
        return default
    # si ya es string
    if isinstance(item, str):
        return item
    # si es lista, tomar el primero que tenga 'valor'
    if isinstance(item, list) and item:
        head = item[0]
        if isinstance(head, dict) and 'valor' in head:
            return head['valor']
    # si es dict con 'valor'
    if isinstance(item, dict) and 'valor' in item:
        return item['valor']
    return default


def _horarios_sistema():
    inicio = conf_repo.obtener('horario_inicio')
    fin = conf_repo.obtener('horario_fin')
    # Horarios institucionales por defecto: 07:00 a 22:00 (Lunes-Sábado)
    v_ini = _extraer_valor_config(inicio, '07:00')
    v_fin = _extraer_valor_config(fin, '22:00')
    t_inicio = parse_time_str(v_ini)
    t_fin = parse_time_str(v_fin)
    return t_inicio, t_fin


def _int_from_conf(nombre: str, default_value: int) -> int:
    try:
        item = conf_repo.obtener(nombre)
        raw = _extraer_valor_config(item, str(default_value))
        return int(str(raw).strip())
    except Exception:
        return default_value


def _coerce_time(value) -> time:
    """Acepta valores tipo str 'HH:MM', datetime.time, o datetime.timedelta y devuelve datetime.time."""
    if value is None:
        raise ValueError('Hora inválida')
    if isinstance(value, str):
        return parse_time_str(value[:5])
    if isinstance(value, time):
        return value
    # MySQL connector puede mapear TIME a timedelta
    if isinstance(value, dt_timedelta):
        total_seconds = int(value.total_seconds())
        hh = (total_seconds // 3600) % 24
        mm = (total_seconds % 3600) // 60
        return parse_time_str(f"{hh:02d}:{mm:02d}")
    # fallback
    return parse_time_str(str(value)[:5])


def _hoy() -> date:
    """Punto único para obtener la fecha actual (testeable)."""
    return datetime.now().date()


def consultar_disponibilidad(recurso_id: int, fecha: str) -> Dict:
    """Devuelve el recurso y reservas vigentes del día. Robusto ante entradas inválidas."""
    try:
        from datetime import datetime as dt, timedelta as td
        # Obtener TODAS las reservas vigentes del día para ese recurso
        reservas_del_dia = reserva_repo.listar_por_recurso_fecha(recurso_id, fecha)
        print(f"DEBUG consultar_disponibilidad: recurso_id={recurso_id}, fecha={fecha}, encontradas={len(reservas_del_dia)} reservas")
        
        # Convertir reservas a formato serializable
        reservas_serializables = []
        ahora = dt.now()
        
        for c in reservas_del_dia:
            # Limpiar formato de hora (quitar segundos y microsegundos)
            hora_inicio_raw = c.get('hora_inicio')
            hora_fin_raw = c.get('hora_fin')
            
            # Convertir a string HH:MM
            if isinstance(hora_inicio_raw, td):
                total_sec = int(hora_inicio_raw.total_seconds())
                hora_inicio_str = f"{total_sec // 3600:02d}:{(total_sec % 3600) // 60:02d}"
            else:
                hora_inicio_str = str(hora_inicio_raw)[:5] if hora_inicio_raw else ''
            
            if isinstance(hora_fin_raw, td):
                total_sec = int(hora_fin_raw.total_seconds())
                hora_fin_str = f"{total_sec // 3600:02d}:{(total_sec % 3600) // 60:02d}"
            else:
                hora_fin_str = str(hora_fin_raw)[:5] if hora_fin_raw else ''
            
            print(f"  - Reserva: {hora_inicio_str} a {hora_fin_str}, estado_bd={c.get('estado')}")
            
            reservas_serializables.append({
                'hora_inicio': hora_inicio_str,
                'hora_fin': hora_fin_str,
                'usuario': f"{c.get('usuario_nombre', '')} {c.get('usuario_apellido', '')}".strip() or 'N/A',
                'estado': c.get('estado', 'PENDIENTE')
            })
        
        print(f"  Total reservas serializables: {len(reservas_serializables)}")
    except Exception as e:
        print(f"ERROR al obtener reservas del día: {e}")
        import traceback
        traceback.print_exc()
        reservas_serializables = []
    recurso = recurso_repo.obtener(recurso_id)
    return {'recurso': recurso, 'reservas': reservas_serializables}


def _recurso_en_mantenimiento(recurso: dict) -> bool:
    """True si el recurso está actualmente en mantenimiento vigente."""
    if recurso['estado'] not in ('EN_MANTENIMIENTO', 'FUERA_DE_SERVICIO'):
        return False
    mant_inicio = recurso.get('mantenimiento_inicio')
    mant_fin = recurso.get('mantenimiento_fin')
    if not mant_inicio or not mant_fin:
        # Sin rango definido, considerar en mantenimiento si el estado así lo indica
        return True
    now = datetime.now()
    # Convertir a datetime si son strings
    if isinstance(mant_inicio, str):
        mant_inicio = datetime.strptime(mant_inicio, '%Y-%m-%d %H:%M:%S')
    if isinstance(mant_fin, str):
        mant_fin = datetime.strptime(mant_fin, '%Y-%m-%d %H:%M:%S')
    return mant_inicio <= now < mant_fin


def _validar_conflictos(recurso_id: int, fecha: str, h_ini: str, h_fin: str) -> Tuple[bool, str]:
    if not h_ini or not h_fin:
        return False, 'Horario no especificado'
    try:
        t_ini, t_fin = parse_time_str(h_ini), parse_time_str(h_fin)
    except (ValueError, TypeError):
        return False, 'Formato de hora inválido'

    if not validate_slot(t_ini, t_fin):
        return False, 'Horario inválido'
    hs_inicio, hs_fin = _horarios_sistema()
    if not (hs_inicio <= t_ini < t_fin <= hs_fin):
        return False, 'Fuera del horario permitido del sistema'
    # Duración mínima/máxima (configurable, default 15-120 min)
    min_min = _int_from_conf('reserva_duracion_min_min', 15)
    max_min = _int_from_conf('reserva_duracion_max_min', 120)
    dur_minutos = (t_fin.hour*60 + t_fin.minute) - (t_ini.hour*60 + t_ini.minute)
    if dur_minutos < min_min or dur_minutos > max_min:
        return False, 'La duración debe ser entre 15 minutos y 2 horas'
    # Validación de día (solo Lunes-Sábado) y ventana máxima de anticipación 7 días.
    try:
        fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
        if fecha_dt.weekday() == 6:  # Domingo
            return False, 'No se permiten reservas en domingo'
        hoy = _hoy()
        # no antes de hoy (control defensivo) y no más de 7 días
        if fecha_dt < hoy:
            return False, 'La fecha no puede ser anterior a hoy'
        # Si es hoy, validar que hora_inicio no esté en el pasado
        if fecha_dt == hoy:
            ahora = datetime.now().time()
            if t_ini <= ahora:
                return False, 'No se puede reservar una hora que ya pasó'
        max_dias = _int_from_conf('reserva_anticipacion_max_dias', 7)
        if (fecha_dt - hoy).days > max_dias:
            return False, f'Solo se permite reservar con hasta {max_dias} días de anticipación'
    except Exception:
        return False, 'Fecha inválida'
    recurso = recurso_repo.obtener(recurso_id)
    if not recurso or recurso['eliminado']:
        return False, 'Recurso no disponible'
    if _recurso_en_mantenimiento(recurso):
        return False, 'El recurso está en mantenimiento en este momento'
    conflictos = reserva_repo.listar_conflictos(recurso_id, fecha, h_ini, h_fin)
    if conflictos:
        return False, 'Existe un conflicto con otra reserva'
    # Validar que el usuario no tenga reservas en el mismo horario (otro recurso)
    user_id = session.get('user_id')
    if user_id:
        # 1. Verificar si es titular de otra reserva
        user_conflicts = reserva_repo.listar_conflictos_usuario(user_id, fecha, h_ini, h_fin)
        if user_conflicts:
            return False, 'Ya tienes una reserva en ese horario para otro recurso'
        
        # 2. Verificar si es acompañante en otra reserva
        companion_conflicts = reserva_repo.listar_conflictos_como_acompanante(user_id, fecha, h_ini, h_fin)
        if companion_conflicts:
            return False, 'Ya estás registrado como acompañante en otra reserva durante este horario'
            
    return True, 'OK'


def crear_reserva(recurso_id: int, fecha: str, hora_inicio: str, hora_fin: str, acompanantes: List[int] = None) -> Tuple[bool, str]:
    user_id = session.get('user_id')
    
    # Validar que el usuario no esté bloqueado o sancionado
    usuario = user_repo.get_by_id(user_id)
    if not usuario:
        return False, 'Usuario no encontrado'
    if usuario.get('estado') == 'BLOQUEADO':
        return False, 'No puedes realizar reservas mientras estés bloqueado'
    
    ok, msg = _validar_conflictos(recurso_id, fecha, hora_inicio, hora_fin)
    if not ok:
        return False, msg
    
    # Validaciones de acompañantes
    recurso = recurso_repo.obtener(recurso_id)
    zona_id = recurso.get('zona_id')
    
    acompanantes_filtrados = []
    if acompanantes:
        acompanantes_filtrados = [uid for uid in acompanantes if uid != user_id]
    
    num_acompanantes = len(acompanantes_filtrados)
    
    if zona_id == 1: # Chill Zone
        if num_acompanantes < 1:
            return False, 'Para Chill Zone se requiere mínimo 1 acompañante'
        if num_acompanantes > 5:
            return False, 'Para Chill Zone el máximo es 5 acompañantes'
    elif zona_id == 2: # Coworking
        # Max 25 personas (1 titular + 24 acompañantes)
        if (num_acompanantes + 1) > 25:
            return False, 'Para Coworking el máximo es 25 personas en total'
    
    # Validar que los acompañantes no tengan reservas en ese horario
    for a_id in acompanantes_filtrados:
        # 1. Verificar si es titular
        conflicts = reserva_repo.listar_conflictos_usuario(a_id, fecha, hora_inicio, hora_fin)
        if conflicts:
            a_user = user_repo.get_by_id(a_id)
            nombre_a = f"{a_user.get('nombre')} {a_user.get('apellido')}" if a_user else f"Usuario {a_id}"
            return False, f'El acompañante {nombre_a} ya tiene una reserva como titular en ese horario'
        
        # 2. Verificar si es acompañante en otra reserva
        comp_conflicts = reserva_repo.listar_conflictos_como_acompanante(a_id, fecha, hora_inicio, hora_fin)
        if comp_conflicts:
            a_user = user_repo.get_by_id(a_id)
            nombre_a = f"{a_user.get('nombre')} {a_user.get('apellido')}" if a_user else f"Usuario {a_id}"
            return False, f'El acompañante {nombre_a} ya está registrado como acompañante en otra reserva durante este horario'

    reserva_id = reserva_repo.crear(user_id, recurso_id, fecha, hora_inicio, hora_fin)
    
    # Agregar acompañantes si se proporcionaron
    if acompanantes_filtrados:
        reserva_repo.agregar_acompanantes(reserva_id, acompanantes_filtrados)
    
    return True, 'Reserva creada'


def modificar_reserva(reserva_id: int, hora_inicio: str, hora_fin: str) -> Tuple[bool, str]:
    res = reserva_repo.obtener(reserva_id)
    if not res or res['estado'] not in ['PENDIENTE', 'ACTIVA']:
        return False, 'Reserva no válida para modificación'
    ok, msg = _validar_conflictos(res['recurso_id'], res['fecha'], hora_inicio, hora_fin)
    if not ok:
        return False, msg
    reserva_repo.actualizar_horario(reserva_id, hora_inicio, hora_fin)
    return True, 'Reserva modificada'


def cancelar_reserva(reserva_id: int) -> Tuple[bool, str]:
    res = reserva_repo.obtener(reserva_id)
    if not res or res['estado'] not in ['PENDIENTE', 'ACTIVA']:
        return False, 'No se puede cancelar'
    # Regla CU-08: no cancelar si ya inició el uso o si falta < 10 minutos
    # 1) Si existe un uso activo, no cancelar
    uso_activo = uso_repo.obtener_activo_por_reserva(reserva_id)
    if uso_activo:
        return False, 'No se puede cancelar una reserva en uso'
    # 2) Ventana mínima de 1 hora antes de la hora de inicio
    try:
        fecha_dt = datetime.strptime(str(res['fecha']), '%Y-%m-%d').date()
    except ValueError:
        # si ya es date
        fecha_dt = res['fecha']
    hi = _coerce_time(res.get('hora_inicio'))
    inicio_dt = datetime.combine(fecha_dt, hi)
    ahora = datetime.now()
    
    # Si ya pasó la hora de inicio, no se puede cancelar (ya debería estar ACTIVA o FINALIZADA)
    if ahora >= inicio_dt:
        return False, 'La reserva ya ha iniciado, no se puede cancelar'
        
    if inicio_dt - ahora < timedelta(hours=1):
        return False, 'Solo se puede cancelar con al menos 1 hora de anticipación'
    
    reserva_repo.cancelar(reserva_id)
    # Notificación (simulada)
    print(f"NOTIFICACION: Reserva {reserva_id} cancelada por el usuario.")
    return True, 'Reserva cancelada exitosamente'


def finalizar_desde_uso(reserva_id: int):
    reserva_repo.marcar_finalizada(reserva_id)


def listar_todas_reservas() -> List[Dict]:
    """Lista todas las reservas del sistema para vista admin."""
    # Asegurar que las reservas expiradas se marquen como FINALIZADA antes de listar
    try:
        reserva_repo.finalizar_expiradas()
    except Exception:
        pass

    reservas = reserva_repo.listar_con_detalles()
    ahora = datetime.now()
    
    # Calcular estado dinámico y cargar acompañantes para cada reserva
    for r in reservas:
        # Cargar acompañantes
        r['acompanantes'] = reserva_repo.listar_acompanantes(r['id'])
        
        if r['estado'] in ['PENDIENTE', 'ACTIVA']:
            fecha_reserva = r['fecha']
            if isinstance(fecha_reserva, str):
                fecha_reserva = datetime.strptime(fecha_reserva, '%Y-%m-%d').date()
            
            hora_inicio_raw = r['hora_inicio']
            hora_fin_raw = r['hora_fin']

            # Helper para convertir a time
            def to_time(val):
                if isinstance(val, timedelta):
                    total_sec = int(val.total_seconds())
                    horas = total_sec // 3600
                    minutos = (total_sec % 3600) // 60
                    return time(horas, minutos)
                elif isinstance(val, str):
                    return datetime.strptime(val, '%H:%M:%S').time()
                return val

            hora_inicio_time = to_time(hora_inicio_raw)
            hora_fin_time = to_time(hora_fin_raw)
            
            datetime_inicio = datetime.combine(fecha_reserva, hora_inicio_time)
            datetime_fin = datetime.combine(fecha_reserva, hora_fin_time)
            
            if ahora < datetime_inicio:
                r['estado'] = 'PENDIENTE'
            elif ahora >= datetime_inicio and ahora < datetime_fin:
                r['estado'] = 'ACTIVA'
            elif ahora >= datetime_fin:
                r['estado'] = 'FINALIZADA'
    
    return reservas


def cancelar_reserva_admin(reserva_id: int) -> Tuple[bool, str]:
    """Admin puede cancelar cualquier reserva sin restricciones de tiempo."""
    res = reserva_repo.obtener(reserva_id)
    if not res:
        return False, 'Reserva no encontrada'
    if res['estado'] not in ['PENDIENTE', 'ACTIVA']:
        return False, 'La reserva no está activa o pendiente'
    
    reserva_repo.cancelar(reserva_id)
    return True, 'Reserva cancelada por administrador'


def listar_reservas_usuario() -> List[dict]:
    # Antes de listar, finalizar automáticamente las reservas expiradas sin uso activo
    try:
        reserva_repo.finalizar_expiradas()
    except Exception:
        pass
    return reserva_repo.listar_por_usuario(session.get('user_id'))
