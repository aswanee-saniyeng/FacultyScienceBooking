from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from datetime import datetime, timedelta
import re

from rooms.models import Room
from bookings.models import Booking
from devices.models import Device


# =========================================================
# CHATBOT HOME
# =========================================================

def chatbot(request):
    return render(request, 'chatbot/chatbot.html')


# =========================================================
# HELPER: CONVERT TIME TO DISPLAY FORMAT
# =========================================================

def format_time(time_value):
    return time_value.strftime('%I:%M %p').lstrip('0')


# =========================================================
# PARSE ROOM AVAILABILITY REQUEST
# =========================================================

def parse_availability_request(message):

    rooms = Room.objects.all()
    found_room = None

    for room in rooms:
        if room.room_name.lower() in message:
            found_room = room
            break

    if not found_room:
        return None

    booking_date = None
    today = timezone.localdate()

    if 'today' in message:
        booking_date = today

    elif 'tomorrow' in message:
        booking_date = today + timedelta(days=1)

    else:
        date_match = re.search(
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            message
        )

        if date_match:
            try:
                year = int(date_match.group(1))
                month = int(date_match.group(2))
                day = int(date_match.group(3))

                booking_date = datetime(
                    year,
                    month,
                    day
                ).date()

            except ValueError:
                return None

    # -----------------------------------------------------
    # TIME FORMAT
    # Example:
    # from 10 AM to 12 PM
    # 10 AM - 12 PM
    # -----------------------------------------------------

    time_match = re.search(
        r'from\s+'
        r'(\d{1,2})'
        r'(?:[:.](\d{2}))?'
        r'\s*(am|pm)'
        r'\s+to\s+'
        r'(\d{1,2})'
        r'(?:[:.](\d{2}))?'
        r'\s*(am|pm)',
        message,
        re.IGNORECASE
    )

    if not time_match:

        time_match = re.search(
            r'(\d{1,2})'
            r'(?:[:.](\d{2}))?'
            r'\s*(am|pm)'
            r'\s*(?:-|to)\s*'
            r'(\d{1,2})'
            r'(?:[:.](\d{2}))?'
            r'\s*(am|pm)',
            message,
            re.IGNORECASE
        )

    if not time_match:
        return None

    start_hour = int(time_match.group(1))
    start_minute = int(time_match.group(2) or 0)
    start_period = time_match.group(3).lower()

    end_hour = int(time_match.group(4))
    end_minute = int(time_match.group(5) or 0)
    end_period = time_match.group(6).lower()

    if start_minute > 59:
        return None

    if end_minute > 59:
        return None

    if start_hour < 1 or start_hour > 12:
        return None

    if end_hour < 1 or end_hour > 12:
        return None

    # Convert AM/PM to 24-hour

    if start_period == 'pm':

        if start_hour != 12:
            start_hour += 12

    elif start_period == 'am':

        if start_hour == 12:
            start_hour = 0

    if end_period == 'pm':

        if end_hour != 12:
            end_hour += 12

    elif end_period == 'am':

        if end_hour == 12:
            end_hour = 0

    try:

        start_time = datetime.strptime(
            f'{start_hour:02d}:{start_minute:02d}',
            '%H:%M'
        ).time()

        end_time = datetime.strptime(
            f'{end_hour:02d}:{end_minute:02d}',
            '%H:%M'
        ).time()

    except ValueError:

        return None

    return {
        'room': found_room,
        'booking_date': booking_date,
        'start_time': start_time,
        'end_time': end_time,
    }


# =========================================================
# PARSE DEVICE AVAILABILITY REQUEST
# =========================================================

def parse_device_availability_request(message):

    devices = Device.objects.all()
    found_device = None

    for device in devices:

        if device.device_name.lower() in message:

            found_device = device
            break

    if not found_device:
        return None

    booking_date = None
    today = timezone.localdate()

    if 'today' in message:

        booking_date = today

    elif 'tomorrow' in message:

        booking_date = today + timedelta(days=1)

    else:

        date_match = re.search(
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            message
        )

        if date_match:

            try:

                year = int(date_match.group(1))
                month = int(date_match.group(2))
                day = int(date_match.group(3))

                booking_date = datetime(
                    year,
                    month,
                    day
                ).date()

            except ValueError:

                return None

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    time_match = re.search(
        r'from\s+'
        r'(\d{1,2})'
        r'(?:[:.](\d{2}))?'
        r'\s*(am|pm)'
        r'\s+to\s+'
        r'(\d{1,2})'
        r'(?:[:.](\d{2}))?'
        r'\s*(am|pm)',
        message,
        re.IGNORECASE
    )

    if not time_match:

        time_match = re.search(
            r'(\d{1,2})'
            r'(?:[:.](\d{2}))?'
            r'\s*(am|pm)'
            r'\s*(?:-|to)\s*'
            r'(\d{1,2})'
            r'(?:[:.](\d{2}))?'
            r'\s*(am|pm)',
            message,
            re.IGNORECASE
        )

    if not time_match:
        return None

    start_hour = int(time_match.group(1))
    start_minute = int(time_match.group(2) or 0)
    start_period = time_match.group(3).lower()

    end_hour = int(time_match.group(4))
    end_minute = int(time_match.group(5) or 0)
    end_period = time_match.group(6).lower()

    if start_minute > 59:
        return None

    if end_minute > 59:
        return None

    if start_hour < 1 or start_hour > 12:
        return None

    if end_hour < 1 or end_hour > 12:
        return None

    # Convert AM/PM

    if start_period == 'pm':

        if start_hour != 12:
            start_hour += 12

    elif start_period == 'am':

        if start_hour == 12:
            start_hour = 0

    if end_period == 'pm':

        if end_hour != 12:
            end_hour += 12

    elif end_period == 'am':

        if end_hour == 12:
            end_hour = 0

    try:

        start_time = datetime.strptime(
            f'{start_hour:02d}:{start_minute:02d}',
            '%H:%M'
        ).time()

        end_time = datetime.strptime(
            f'{end_hour:02d}:{end_minute:02d}',
            '%H:%M'
        ).time()

    except ValueError:

        return None

    return {
        'device': found_device,
        'booking_date': booking_date,
        'start_time': start_time,
        'end_time': end_time,
    }


# =========================================================
# SAVE PENDING CHATBOT BOOKING
# =========================================================

def save_pending_booking(
    request,
    resource_type,
    resource_id,
    booking_date,
    start_time,
    end_time
):

    request.session['chatbot_pending_booking'] = {
        'resource_type': resource_type,
        'resource_id': resource_id,
        'booking_date': booking_date.isoformat(),
        'start_time': start_time.strftime('%H:%M'),
        'end_time': end_time.strftime('%H:%M'),
    }

    request.session['chatbot_booking_step'] = 'confirmation'

    request.session.modified = True


# =========================================================
# CHATBOT API
# =========================================================

def chatbot_api(request):

    if request.method != 'POST':

        return JsonResponse({
            'reply': 'Invalid request method.'
        })

    message = request.POST.get(
        'message',
        ''
    ).strip().lower()

    if not message:

        return JsonResponse({
            'reply': 'Please enter a message.'
        })


    # =====================================================
    # STEP 1
    # HANDLE EXISTING CHATBOT BOOKING
    # =====================================================

    pending_booking = request.session.get(
        'chatbot_pending_booking'
    )

    booking_step = request.session.get(
        'chatbot_booking_step'
    )


    # =====================================================
    # CONFIRMATION
    # =====================================================

    if (
        pending_booking
        and booking_step == 'confirmation'
    ):

        yes_words = [
            'yes',
            'yeah',
            'yep',
            'sure',
            'ok',
            'okay',
            'confirm',
            'confirmed',
            'book it',
            'do it',
            'ยืนยัน',
            'ใช่',
            'ตกลง',
            'จองเลย'
        ]

        no_words = [
            'no',
            'nope',
            'cancel',
            'stop',
            'ไม่',
            'ยกเลิก'
        ]

        if message in yes_words:

            request.session['chatbot_booking_step'] = 'purpose'

            request.session.modified = True

            return JsonResponse({
                'reply': """
                <strong>Great!</strong>

                <br><br>

                Please enter the <strong>purpose</strong>
                of this booking.

                <br><br>

                Example:
                <br>

                <strong>
                Science class
                </strong>

                <br>

                or

                <br>

                <strong>
                Laboratory experiment
                </strong>
                """
            })


        if message in no_words:

            request.session.pop(
                'chatbot_pending_booking',
                None
            )

            request.session.pop(
                'chatbot_booking_step',
                None
            )

            request.session.modified = True

            return JsonResponse({
                'reply': """
                The booking request has been cancelled.

                <br><br>

                You can ask me to check another room
                or device.
                """
            })


        return JsonResponse({
            'reply': """
            Please confirm your booking.

            <br><br>

            <strong>
            Yes
            </strong>
            - continue booking

            <br>

            <strong>
            No
            </strong>
            - cancel
            """
        })


    # =====================================================
    # PURPOSE
    # =====================================================

    if (
        pending_booking
        and booking_step == 'purpose'
    ):

        purpose = message.strip()

        if len(purpose) < 2:

            return JsonResponse({
                'reply': """
                Please enter a valid purpose
                for the booking.
                """
            })


        # -------------------------------------------------
        # LOGIN CHECK
        # -------------------------------------------------

        if not request.user.is_authenticated:

            request.session.pop(
                'chatbot_pending_booking',
                None
            )

            request.session.pop(
                'chatbot_booking_step',
                None
            )

            request.session.modified = True

            return JsonResponse({
                'reply': """
                Please login before creating a booking.

                <br><br>

                After logging in, please start
                the booking request again.
                """
            })


        # -------------------------------------------------
        # GET DATA FROM SESSION
        # -------------------------------------------------

        try:

            resource_type = pending_booking[
                'resource_type'
            ]

            resource_id = int(
                pending_booking['resource_id']
            )

            booking_date = datetime.strptime(
                pending_booking['booking_date'],
                '%Y-%m-%d'
            ).date()

            start_time = datetime.strptime(
                pending_booking['start_time'],
                '%H:%M'
            ).time()

            end_time = datetime.strptime(
                pending_booking['end_time'],
                '%H:%M'
            ).time()

        except (KeyError, ValueError, TypeError):

            request.session.pop(
                'chatbot_pending_booking',
                None
            )

            request.session.pop(
                'chatbot_booking_step',
                None
            )

            request.session.modified = True

            return JsonResponse({
                'reply': """
                Sorry, the booking information
                is no longer valid.

                <br><br>

                Please start the booking again.
                """
            })


        # =================================================
        # ROOM BOOKING
        # =================================================

        if resource_type == 'room':

            try:

                room = Room.objects.get(
                    id=resource_id
                )

            except Room.DoesNotExist:

                request.session.pop(
                    'chatbot_pending_booking',
                    None
                )

                request.session.pop(
                    'chatbot_booking_step',
                    None
                )

                request.session.modified = True

                return JsonResponse({
                    'reply': 'The selected room no longer exists.'
                })


            # Re-check availability

            conflicting_bookings = Booking.objects.filter(
                room=room,
                booking_date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(
                status__in=[
                    'cancelled',
                    'rejected'
                ]
            )

            if (
                room.status != 'available'
                or conflicting_bookings.exists()
            ):

                request.session.pop(
                    'chatbot_pending_booking',
                    None
                )

                request.session.pop(
                    'chatbot_booking_step',
                    None
                )

                request.session.modified = True

                return JsonResponse({
                    'reply': f"""
                    Sorry, <strong>{room.room_name}</strong>
                    is no longer available for this time.

                    <br><br>

                    Please check another time or room.
                    """
                })


            # Create booking

            booking = Booking.objects.create(
                user=request.user,
                room=room,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                status='pending'
            )


            # Clear session

            request.session.pop(
                'chatbot_pending_booking',
                None
            )

            request.session.pop(
                'chatbot_booking_step',
                None
            )

            request.session.modified = True


            return JsonResponse({
                'reply': f"""
                <strong>Booking created successfully!</strong>

                <br><br>

                Room:
                <strong>{room.room_name}</strong>

                <br>

                Date:
                <strong>{booking_date}</strong>

                <br>

                Time:
                <strong>
                {format_time(start_time)}
                -
                {format_time(end_time)}
                </strong>

                <br>

                Purpose:
                <strong>{purpose}</strong>

                <br>

                Status:
                <strong>Pending</strong>

                <br><br>

                Your booking is waiting for
                <strong>Admin approval</strong>.
                """
            })


        # =================================================
        # DEVICE BOOKING
        # =================================================

        elif resource_type == 'device':

            try:

                device = Device.objects.get(
                    id=resource_id
                )

            except Device.DoesNotExist:

                request.session.pop(
                    'chatbot_pending_booking',
                    None
                )

                request.session.pop(
                    'chatbot_booking_step',
                    None
                )

                request.session.modified = True

                return JsonResponse({
                    'reply': 'The selected device no longer exists.'
                })


            # Re-check device availability

            conflicting_bookings = Booking.objects.filter(
                device=device,
                booking_date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(
                status__in=[
                    'cancelled',
                    'rejected'
                ]
            )


            if (
                device.status != 'available'
                or conflicting_bookings.exists()
            ):

                request.session.pop(
                    'chatbot_pending_booking',
                    None
                )

                request.session.pop(
                    'chatbot_booking_step',
                    None
                )

                request.session.modified = True

                return JsonResponse({
                    'reply': f"""
                    Sorry, <strong>{device.device_name}</strong>
                    is no longer available for this time.

                    <br><br>

                    Please check another time or device.
                    """
                })


            # Create booking

            booking = Booking.objects.create(
                user=request.user,
                device=device,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                status='pending'
            )


            # Clear session

            request.session.pop(
                'chatbot_pending_booking',
                None
            )

            request.session.pop(
                'chatbot_booking_step',
                None
            )

            request.session.modified = True


            return JsonResponse({
                'reply': f"""
                <strong>Booking created successfully!</strong>

                <br><br>

                Device:
                <strong>{device.device_name}</strong>

                <br>

                Date:
                <strong>{booking_date}</strong>

                <br>

                Time:
                <strong>
                {format_time(start_time)}
                -
                {format_time(end_time)}
                </strong>

                <br>

                Purpose:
                <strong>{purpose}</strong>

                <br>

                Status:
                <strong>Pending</strong>

                <br><br>

                Your booking is waiting for
                <strong>Admin approval</strong>.
                """
            })


    # =====================================================
    # GREETING
    # =====================================================

    if message in [
        'hello',
        'hi',
        'hey',
        'สวัสดี'
    ] or message.startswith('hello ') \
            or message.startswith('hi ') \
            or message.startswith('hey '):

        reply = """
        Hello! 👋

        <br><br>

        I am the Faculty Science Booking Assistant.

        <br><br>

        I can help you with:

        <br>
        • Check available rooms
        <br>
        • Check available devices
        <br>
        • Check room availability
        <br>
        • Check device availability
        <br>
        • Check your bookings
        <br>
        • Check booking status
        <br>
        • Create a booking
        """

    # =====================================================
    # AVAILABLE ROOMS
    # =====================================================

    elif (
        'which rooms' in message
        or 'available rooms' in message
        or 'what rooms are available' in message
        or 'rooms available' in message
        or 'ห้องไหนว่าง' in message
        or 'ห้องที่ว่าง' in message
    ):

        rooms = Room.objects.filter(
            status='available'
        )

        if rooms.exists():

            room_list = '<br>'.join(
                [
                    f'• {room.room_name} '
                    f'({room.building}) '
                    f'- Capacity: {room.capacity}'
                    for room in rooms
                ]
            )

            reply = f"""
            <strong>Available Rooms:</strong>

            <br><br>

            {room_list}
            """

        else:

            reply = """
            There are currently no available rooms.
            """

    # =====================================================
    # AVAILABLE DEVICES
    # =====================================================

    elif (
        'which devices' in message
        or 'available devices' in message
        or 'what devices are available' in message
        or 'devices available' in message
        or 'อุปกรณ์ไหนว่าง' in message
        or 'อุปกรณ์ที่ว่าง' in message
    ):

        devices = Device.objects.filter(
            status='available'
        )

        if devices.exists():

            device_list = '<br>'.join(
                [
                    f'• {device.device_name} '
                    f'- Quantity: {device.quantity}'
                    for device in devices
                ]
            )

            reply = f"""
            <strong>Available Devices:</strong>

            <br><br>

            {device_list}
            """

        else:

            reply = """
            There are currently no available devices.
            """

    # =====================================================
    # CHECK DEVICE AVAILABILITY
    # =====================================================

    elif (
        (
            'can i book' in message
            or 'can i reserve' in message
            or 'is available' in message
            or 'available at' in message
            or 'available on' in message
            or 'จองได้ไหม' in message
            or 'ว่างไหม' in message
        )
        and any(
            device.device_name.lower() in message
            for device in Device.objects.all()
        )
    ):

        availability = parse_device_availability_request(
            message
        )

        if not availability:

            reply = """
            I need more information to check device availability.

            <br><br>

            Please include:

            <br>
            • Device name
            <br>
            • Date
            <br>
            • Start and end time

            <br><br>

            Example:

            <br>

            <strong>
            Can I book the Projector tomorrow
            from 10 AM to 12 PM?
            </strong>
            """

        else:

            device = availability['device']
            booking_date = availability['booking_date']
            start_time = availability['start_time']
            end_time = availability['end_time']

            if not booking_date:

                reply = """
                Please provide the booking date.

                <br><br>

                Example:

                <br>

                <strong>
                Can I book the Projector tomorrow
                from 10 AM to 12 PM?
                </strong>
                """

            elif start_time >= end_time:

                reply = """
                The end time must be later
                than the start time.

                <br><br>

                Example:

                <br>

                <strong>
                10 AM to 12 PM
                </strong>
                """

            else:

                if device.status != 'available':

                    reply = f"""
                    <strong>
                    {device.device_name}
                    is currently unavailable.
                    </strong>

                    <br><br>

                    Please choose another device.
                    """

                else:

                    conflicting_bookings = Booking.objects.filter(
                        device=device,
                        booking_date=booking_date,
                        start_time__lt=end_time,
                        end_time__gt=start_time
                    ).exclude(
                        status__in=[
                            'cancelled',
                            'rejected'
                        ]
                    )

                    if conflicting_bookings.exists():

                        reply = f"""
                        <strong>
                        {device.device_name}
                        is not available.
                        </strong>

                        <br><br>

                        There is already a booking
                        for this device during this time.

                        <br><br>

                        Requested date:

                        <strong>
                        {booking_date}
                        </strong>

                        <br>

                        Requested time:

                        <strong>
                        {format_time(start_time)}
                        -
                        {format_time(end_time)}
                        </strong>

                        <br><br>

                        Please choose another time
                        or another device.
                        """

                    else:

                        # Save booking request
                        save_pending_booking(
                            request,
                            'device',
                            device.id,
                            booking_date,
                            start_time,
                            end_time
                        )

                        reply = f"""
                        <strong>
                        {device.device_name} is available.
                        </strong>

                        <br><br>

                        Date:

                        <strong>
                        {booking_date}
                        </strong>

                        <br>

                        Time:

                        <strong>
                        {format_time(start_time)}
                        -
                        {format_time(end_time)}
                        </strong>

                        <br>

                        Quantity available:

                        <strong>
                        {device.quantity}
                        </strong>

                        <br><br>

                        Would you like to book this device?

                        <br><br>

                        Please answer:

                        <strong>
                        Yes
                        </strong>
                        or
                        <strong>
                        No
                        </strong>
                        """

    # =====================================================
    # CHECK ROOM AVAILABILITY
    # =====================================================

    elif (
        (
            'can i book' in message
            or 'can i reserve' in message
            or 'is available' in message
            or 'available at' in message
            or 'available on' in message
            or 'จองได้ไหม' in message
            or 'ว่างไหม' in message
        )
        and any(
            room.room_name.lower() in message
            for room in Room.objects.all()
        )
    ):

        availability = parse_availability_request(
            message
        )

        if not availability:

            reply = """
            I need more information to check room availability.

            <br><br>

            Please include:

            <br>
            • Room name
            <br>
            • Date
            <br>
            • Start and end time

            <br><br>

            Example:

            <br>

            <strong>
            Can I book Room 203 tomorrow
            from 10 AM to 12 PM?
            </strong>
            """

        else:

            room = availability['room']
            booking_date = availability['booking_date']
            start_time = availability['start_time']
            end_time = availability['end_time']

            if not booking_date:

                reply = """
                Please provide the booking date.

                <br><br>

                Example:

                <br>

                <strong>
                Can I book Room 203 tomorrow
                from 10 AM to 12 PM?
                </strong>
                """

            elif start_time >= end_time:

                reply = """
                The end time must be later
                than the start time.

                <br><br>

                Example:

                <br>

                <strong>
                10 AM to 12 PM
                </strong>
                """

            else:

                if room.status != 'available':

                    reply = f"""
                    <strong>
                    Room {room.room_name}
                    is currently unavailable.
                    </strong>

                    <br><br>

                    Please choose another room.
                    """

                else:

                    conflicting_bookings = Booking.objects.filter(
                        room=room,
                        booking_date=booking_date,
                        start_time__lt=end_time,
                        end_time__gt=start_time
                    ).exclude(
                        status__in=[
                            'cancelled',
                            'rejected'
                        ]
                    )

                    if conflicting_bookings.exists():

                        reply = f"""
                        <strong>
                        Room {room.room_name}
                        is not available.
                        </strong>

                        <br><br>

                        There is already a booking
                        during this time.

                        <br><br>

                        Requested date:

                        <strong>
                        {booking_date}
                        </strong>

                        <br>

                        Requested time:

                        <strong>
                        {format_time(start_time)}
                        -
                        {format_time(end_time)}
                        </strong>

                        <br><br>

                        Please choose another time
                        or another room.
                        """

                    else:

                        # Save booking request
                        save_pending_booking(
                            request,
                            'room',
                            room.id,
                            booking_date,
                            start_time,
                            end_time
                        )

                        reply = f"""
                        <strong>
                        Room {room.room_name}
                        is available.
                        </strong>

                        <br><br>

                        Date:

                        <strong>
                        {booking_date}
                        </strong>

                        <br>

                        Time:

                        <strong>
                        {format_time(start_time)}
                        -
                        {format_time(end_time)}
                        </strong>

                        <br><br>

                        Would you like to book this room?

                        <br><br>

                        Please answer:

                        <strong>
                        Yes
                        </strong>
                        or
                        <strong>
                        No
                        </strong>
                        """

    # =====================================================
    # SPECIFIC BOOKING STATUS
    # =====================================================

    elif (
        'status of my room' in message
        or 'status of my booking for room' in message
        or 'room booking status' in message
    ):

        room_number_match = re.search(
            r'room\s+([a-zA-Z0-9_-]+)',
            message,
            re.IGNORECASE
        )

        if room_number_match:

            room_name = room_number_match.group(1)

            bookings = Booking.objects.filter(
                user=request.user,
                room__room_name__iexact=room_name
            ).exclude(
                status='rejected'
            ).order_by(
                '-booking_date',
                '-start_time'
            )

            if bookings.exists():

                booking_list = '<br><br>'.join(
                    [
                        f"""
                        <strong>
                        Room {booking.room.room_name}
                        </strong>

                        <br>

                        Date:
                        {booking.booking_date}

                        <br>

                        Time:
                        {format_time(booking.start_time)}
                        -
                        {format_time(booking.end_time)}

                        <br>

                        Purpose:
                        {booking.purpose}

                        <br>

                        Status:
                        <strong>
                        {booking.status.title()}
                        </strong>
                        """
                        for booking in bookings
                    ]
                )

                reply = f"""
                <strong>
                Your bookings for Room {room_name}:
                </strong>

                <br><br>

                {booking_list}
                """

            else:

                reply = f"""
                You have no bookings for Room {room_name}.
                """

        else:

            reply = """
            Please specify the room number.

            <br><br>

            Example:

            <br>

            <strong>
            What is the status of my Room 203 booking?
            </strong>
            """

    # =====================================================
    # SPECIFIC ROOM
    # =====================================================

    elif 'room' in message:

        room_number_match = re.search(
            r'room\s+([a-zA-Z0-9_-]+)',
            message,
            re.IGNORECASE
        )

        if room_number_match:

            room_name = room_number_match.group(1)

            try:

                room = Room.objects.get(
                    room_name__iexact=room_name
                )

                reply = f"""
                <strong>
                Room {room.room_name}
                </strong>

                <br><br>

                Building:
                {room.building}

                <br>

                Capacity:
                {room.capacity}

                <br>

                Status:
                <strong>
                {room.status.title()}
                </strong>

                <br>

                Description:
                {room.description}
                """

            except Room.DoesNotExist:

                reply = f"""
                I could not find Room {room_name}.
                """

        else:

            reply = """
            Please specify the room number.

            <br><br>

            Example:

            <br>

            <strong>
            Tell me about Room 203
            </strong>
            """

    # =====================================================
    # GENERAL BOOKING STATUS
    # =====================================================

    elif (
        'booking status' in message
        or 'status of my booking' in message
        or 'what is the status' in message
    ):

        if not request.user.is_authenticated:

            reply = """
            Please login to check your booking status.
            """

        else:

            bookings = Booking.objects.filter(
                user=request.user
            ).order_by(
                '-booking_date',
                '-start_time'
            )

            if bookings.exists():

                booking_list = '<br><br>'.join(
                    [
                        f"""
                        <strong>
                        {booking.room.room_name
                        if booking.room
                        else booking.device.device_name}
                        </strong>

                        <br>

                        Date:
                        {booking.booking_date}

                        <br>

                        Time:
                        {format_time(booking.start_time)}
                        -
                        {format_time(booking.end_time)}

                        <br>

                        Purpose:
                        {booking.purpose}

                        <br>

                        Status:
                        <strong>
                        {booking.status.title()}
                        </strong>
                        """
                        for booking in bookings
                    ]
                )

                reply = f"""
                <strong>
                Your Booking Status:
                </strong>

                <br><br>

                {booking_list}
                """

            else:

                reply = """
                You do not have any bookings yet.
                """

    # =====================================================
    # PENDING BOOKINGS
    # =====================================================

    elif (
        'pending booking' in message
        or 'pending bookings' in message
        or 'รออนุมัติ' in message
    ):

        if not request.user.is_authenticated:

            reply = """
            Please login to check your pending bookings.
            """

        else:

            bookings = Booking.objects.filter(
                user=request.user,
                status='pending'
            ).order_by(
                'booking_date',
                'start_time'
            )

            if bookings.exists():

                booking_list = '<br><br>'.join(
                    [
                        f"""
                        <strong>
                        {booking.room.room_name
                        if booking.room
                        else booking.device.device_name}
                        </strong>

                        <br>

                        Date:
                        {booking.booking_date}

                        <br>

                        Time:
                        {format_time(booking.start_time)}
                        -
                        {format_time(booking.end_time)}

                        <br>

                        Purpose:
                        {booking.purpose}

                        <br>

                        Status:
                        <strong>
                        Pending
                        </strong>
                        """
                        for booking in bookings
                    ]
                )

                reply = f"""
                <strong>
                Your Pending Bookings:
                </strong>

                <br><br>

                {booking_list}
                """

            else:

                reply = """
                You do not have any pending bookings.
                """

    # =====================================================
    # MY BOOKINGS
    # =====================================================

    elif (
        'my booking' in message
        or 'my bookings' in message
        or 'รายการจองของฉัน' in message
    ):

        if not request.user.is_authenticated:

            reply = """
            Please login to view your bookings.
            """

        else:

            bookings = Booking.objects.filter(
                user=request.user
            ).order_by(
                '-booking_date',
                '-start_time'
            )

            if bookings.exists():

                booking_list = '<br><br>'.join(
                    [
                        f"""
                        <strong>
                        {booking.room.room_name
                        if booking.room
                        else booking.device.device_name}
                        </strong>

                        <br>

                        Date:
                        {booking.booking_date}

                        <br>

                        Time:
                        {format_time(booking.start_time)}
                        -
                        {format_time(booking.end_time)}

                        <br>

                        Purpose:
                        {booking.purpose}

                        <br>

                        Status:
                        <strong>
                        {booking.status.title()}
                        </strong>
                        """
                        for booking in bookings
                    ]
                )

                reply = f"""
                <strong>
                Your Bookings:
                </strong>

                <br><br>

                {booking_list}
                """

            else:

                reply = """
                You do not have any bookings yet.
                """

    # =====================================================
    # DEVICE BOOKING INSTRUCTIONS
    # =====================================================

    elif (
        'book device' in message
        or 'booking device' in message
        or 'จองอุปกรณ์' in message
    ):

        reply = """
        To book a device, you can ask:

        <br><br>

        <strong>
        Can I book the Projector tomorrow
        from 10 AM to 12 PM?
        </strong>

        <br><br>

        If the device is available,
        I will ask you to confirm the booking.
        """

    # =====================================================
    # ROOM BOOKING INSTRUCTIONS
    # =====================================================

    elif (
        'book room' in message
        or 'booking room' in message
        or 'จองห้อง' in message
    ):

        reply = """
        To book a room, you can ask:

        <br><br>

        <strong>
        Can I book Room 203 tomorrow
        from 10 AM to 12 PM?
        </strong>

        <br><br>

        If the room is available,
        I will ask you to confirm the booking.
        """

    # =====================================================
    # GENERAL BOOKING
    # =====================================================

    elif (
        'book' in message
        or 'reserve' in message
        or 'จอง' in message
    ):

        reply = """
        I can help you make a booking.

        <br><br>

        Please specify:

        <br>
        • Room or device
        <br>
        • Date
        <br>
        • Start time
        <br>
        • End time

        <br><br>

        Example:

        <br>

        <strong>
        Can I book Room 203 tomorrow
        from 10 AM to 12 PM?
        </strong>
        """

    # =====================================================
    # DEFAULT
    # =====================================================

    else:

        reply = """
        I can help you with:

        <br><br>

        • Available rooms
        <br>
        • Available devices
        <br>
        • Room availability
        <br>
        • Device availability
        <br>
        • My bookings
        <br>
        • Pending bookings
        <br>
        • Booking status
        <br>
        • Create a booking

        <br><br>

        Example:

        <br>

        <strong>
        Which rooms are available?
        </strong>

        <br>

        <strong>
        What devices are available?
        </strong>

        <br>

        <strong>
        Can I book Room 203 tomorrow
        from 10 AM to 12 PM?
        </strong>
        """


    # =====================================================
    # RETURN RESPONSE
    # =====================================================

    return JsonResponse({
        'reply': reply
    })