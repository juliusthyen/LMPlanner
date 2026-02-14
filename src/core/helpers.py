# region Helper Functions:

def convert_seconds_to_minutes_time(lap_time):
    minutes, minutes_remainder = divmod(lap_time, 60)
    seconds, seconds_remainder = divmod(minutes_remainder, 1)
    return minutes, seconds, seconds_remainder
    # Convert using:
    # m, s, ms = convert_seconds_to_minutes_time(SECONDS)
    # Format as follows for m.ss.ms:
    # {m:.0f}.{s:02.0f}.{ms*10:.0f}

def convert_seconds_to_hours_time(lap_time):
    hours, hours_remainder = divmod(lap_time, 3600)
    minutes, minutes_remainder = divmod(hours_remainder, 60)
    seconds, seconds_remainder = divmod(minutes_remainder, 1)
    return hours, minutes, seconds, seconds_remainder
    # Convert using:
    # m, s, ms = convert_seconds_to_minutes_time(SECONDS)
    # Format as follows for m.ss.ms:
    # {h:02.0f}:{m:02.0f}.{s:02.0f},{ms*10:.0f}

def get_valid_float(inp):
    try:
        inp = float(inp)
    except ValueError:
        print("Invalid Input.")
        return None
    return inp

def get_valid_int(inp):
    try:
        inp = int(inp)
    except ValueError:
        print("Invalid Input.")
        return None
    return inp

def get_user_confirmation():
    pass
# endregion