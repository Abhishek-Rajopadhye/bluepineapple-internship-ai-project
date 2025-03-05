import uuid

def generate_jitsi_link():
    """
    Generates a unique Jitsi Meet room URL for a VoIP call.
    """
    room_name = f"technician-call-{uuid.uuid4().hex}"  # Unique room name
    return f"https://meet.jit.si/{room_name}"
