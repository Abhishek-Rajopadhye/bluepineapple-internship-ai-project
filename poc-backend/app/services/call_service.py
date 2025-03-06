import uuid

def generate_jitsi_link():
    """
    Generates a unique Jitsi Meet room URL for a VoIP call.

    Returns:
        str: The generated Jitsi Meet room URL.

    Raises:
        Exception: If there is an error generating the Jitsi Meet room URL.
    """
    try:
        room_name = f"technician-call-{uuid.uuid4().hex}"  # Unique room name
        return f"https://meet.jit.si/{room_name}"
    except Exception as linkGenerationError:
        print(f"Error generating Jitsi Meet room URL: {linkGenerationError}")
        raise
