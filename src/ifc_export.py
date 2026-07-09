import uuid, base64
from datetime import datetime

def compress_guid(guid_str):
    # Standard IFC GUID: base64 of UUID bytes
    raw_uuid = uuid.UUID(guid_str).bytes
    return base64.b64encode(raw_uuid, b"-_").decode()[:22]

def export_ifc(design):
    lines = []
    lines.append("ISO-10303-21;")
    lines.append("HEADER;")
    lines.append("FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');")
    lines.append(f"FILE_NAME('','',(''),(''),'IfcOpenShell-v0.7.0','RANDOM V4','');")
    lines.append("FILE_SCHEMA(('IFC2X3'));")
    lines.append("ENDSEC;")
    lines.append("DATA;")
    # ... (entity creation similar to V4 but using compress_guid)
    # ...
    return "\n".join(lines)
