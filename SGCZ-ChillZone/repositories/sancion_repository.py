from typing import List, Dict
from utils.db import query_all, execute

def listar() -> List[Dict]:
    sql = (
        "SELECT s.*, u.nombre as usuario_nombre, u.apellido as usuario_apellido, u.correo as usuario_correo, a.nombre as admin_nombre, "
        "i.descripcion as incidencia_desc, i.creado_en as incidencia_fecha, "
        "ui.nombre as reportado_por_nombre, ui.apellido as reportado_por_apellido, "
        "CASE "
        "  WHEN s.estado = 'LEVANTADA' AND s.levantada_en IS NOT NULL THEN s.levantada_en "
        "  ELSE DATE_ADD(s.creado_en, INTERVAL CASE s.tipo "
        "    WHEN 'LEVE' THEN 3 WHEN 'GRAVE' THEN 7 WHEN 'CRITICA' THEN 14 ELSE 0 END DAY) "
        "END as fecha_fin "
        "FROM sanciones s "
        "JOIN usuarios u ON u.id=s.usuario_id "
        "JOIN usuarios a ON a.id=s.creado_por "
        "LEFT JOIN incidencias i ON i.id=s.incidencia_id "
        "LEFT JOIN usuarios ui ON ui.id=i.usuario_id "
        "ORDER BY s.creado_en DESC"
    )
    return query_all(sql)

def listar_por_usuario(usuario_id: int) -> List[Dict]:
    sql = (
        "SELECT s.*, u.nombre as usuario_nombre, u.apellido as usuario_apellido, a.nombre as admin_nombre, i.descripcion as incidencia_desc, "
        "CASE "
        "  WHEN s.estado = 'LEVANTADA' AND s.levantada_en IS NOT NULL THEN s.levantada_en "
        "  ELSE DATE_ADD(s.creado_en, INTERVAL CASE s.tipo "
        "    WHEN 'LEVE' THEN 3 WHEN 'GRAVE' THEN 7 WHEN 'CRITICA' THEN 14 ELSE 0 END DAY) "
        "END as fecha_fin "
        "FROM sanciones s JOIN usuarios u ON u.id=s.usuario_id "
        "JOIN usuarios a ON a.id=s.creado_por "
        "LEFT JOIN incidencias i ON i.id=s.incidencia_id "
        "WHERE s.usuario_id=%s ORDER BY s.creado_en DESC"
    )
    return query_all(sql, (usuario_id,))

def crear(usuario_id: int, creado_por: int, motivo: str, tipo: str, puntos: int, incidencia_id: int = None) -> int:
    sql = "INSERT INTO sanciones (usuario_id, creado_por, motivo, tipo, puntos, estado, incidencia_id) VALUES (%s,%s,%s,%s,%s,'ACTIVA', %s)"
    return execute(sql, (usuario_id, creado_por, motivo, tipo, puntos, incidencia_id))

def levantar(sancion_id: int):
    execute("UPDATE sanciones SET estado='LEVANTADA', levantada_en=NOW() WHERE id=%s AND estado='ACTIVA'", (sancion_id,))
