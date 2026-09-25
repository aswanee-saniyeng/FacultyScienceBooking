from django.http import JsonResponse
from django.shortcuts import render

from rooms.models import Room
from bookings.models import Booking
from devices.models import Device


def chatbot(request):
    return render(request, 'chatbot/chatbot.html')


def chatbot_api(request):

    if request.method != 'POST':
        return JsonResponse(
            {'reply': 'Invalid request.'},
            status=400
        )

    message = request.POST.get('message', '').strip().lower()

    if not message:
        return JsonResponse({
            'reply': 'Please enter a question.'
        })


    # ==========================================
    # GREETING
    # ==========================================

    if (
        message in ['hello', 'hi']
        or message.startswith('hello ')
        or message.startswith('hi ')
        or 'สวัสดี' in message
    ):

        reply = """
        👋 Hello!

        I am the Faculty Science Booking Assistant.

        You can ask me about room availability,
        devices, room booking, and booking status.
        """


    # ==========================================
    # AVAILABLE ROOMS
    # ==========================================

    elif (
        'available room' in message
        or 'available rooms' in message
        or 'room availability' in message
        or 'which rooms' in message
        or 'ห้องว่าง' in message
    ):

        rooms = Room.objects.filter(
            status='available'
        )

        if rooms.exists():

            reply = """
            <strong>Available Rooms:</strong>
            <br><br>
            """

            for room in rooms:

                reply += f"""
                • <strong>Room {room.room_name}</strong>
                <br>
                Building: {room.building}
                <br>
                Capacity: {room.capacity}
                <br><br>
                """

        else:

            reply = """
            There are currently no available rooms.
            """


    # ==========================================
    # AVAILABLE DEVICES
    # ==========================================

    elif (
        'available device' in message
        or 'available devices' in message
        or 'which devices' in message
        or 'what devices are available' in message
        or 'device availability' in message
        or 'อุปกรณ์ที่ว่าง' in message
        or 'มีอุปกรณ์อะไรบ้าง' in message
    ):

        devices = Device.objects.filter(
            status='available'
        )

        if devices.exists():

            reply = """
            <strong>Available Devices:</strong>
            <br><br>
            """

            for device in devices:

                reply += f"""
                • <strong>{device.device_name}</strong>
                <br>
                Type: {device.device_type}
                <br>
                Quantity: {device.quantity}
                """

                if device.description:

                    reply += f"""
                    <br>
                    Description: {device.description}
                    """

                reply += """
                <br><br>
                """

        else:

            reply = """
            There are currently no available devices.
            """


    # ==========================================
    # SPECIFIC BOOKING STATUS
    # ==========================================

    elif (
        'status of my room' in message
        or 'status of my booking for room' in message
        or 'my room' in message and 'booking status' in message
        or 'สถานะการจองห้อง' in message
    ):

        if not request.user.is_authenticated:

            reply = """
            Please login first to check your booking status.
            """

        else:

            rooms = Room.objects.all()

            found_room = None

            for room in rooms:

                if room.room_name.lower() in message:

                    found_room = room
                    break

            if found_room:

                bookings = Booking.objects.filter(
                    user=request.user,
                    room=found_room
                ).order_by(
                    '-booking_date',
                    '-start_time'
                )

                if bookings.exists():

                    reply = f"""
                    <strong>Booking Status for Room {found_room.room_name}:</strong>
                    <br><br>
                    """

                    for booking in bookings:

                        status = booking.status.capitalize()

                        reply += f"""
                        • <strong>Room {found_room.room_name}</strong>
                        <br>
                        Date: {booking.booking_date}
                        <br>
                        Time: {booking.start_time} - {booking.end_time}
                        <br>
                        Purpose: {booking.purpose}
                        <br>
                        Status: <strong>{status}</strong>
                        <br><br>
                        """

                else:

                    reply = f"""
                    You do not have any bookings for
                    <strong>Room {found_room.room_name}</strong>.
                    """

            else:

                reply = """
                I could not find that room.

                <br><br>

                Try asking:
                <br>
                <strong>
                What is the status of my room 203 booking?
                </strong>
                """


    # ==========================================
    # SPECIFIC ROOM
    # ==========================================

    elif 'room' in message:

        rooms = Room.objects.all()

        found_room = None

        for room in rooms:

            if room.room_name.lower() in message:

                found_room = room
                break


        if found_room:

            if found_room.status == 'available':

                reply = f"""
                <strong>Room {found_room.room_name}</strong>
                is currently <strong>available</strong>.
                <br><br>

                Building:
                {found_room.building}

                <br>

                Capacity:
                {found_room.capacity}

                <br><br>

                You can proceed with the booking.
                """

            else:

                reply = f"""
                <strong>Room {found_room.room_name}</strong>
                is currently <strong>unavailable</strong>.
                """

        else:

            reply = """
            I could not find that room.

            <br><br>

            You can ask me:
            <br>
            • Which rooms are available?
            <br>
            • Is room 203 available?
            """


    # ==========================================
    # BOOKING STATUS
    # ==========================================

    elif (
        'booking status' in message
        or 'status of my booking' in message
        or 'what is the status' in message
        or 'check my booking status' in message
        or 'status of my bookings' in message
        or 'สถานะการจอง' in message
    ):

        if not request.user.is_authenticated:

            reply = """
            Please login first to check your booking status.
            """

        else:

            bookings = Booking.objects.filter(
                user=request.user
            ).order_by(
                '-booking_date',
                '-start_time'
            )

            if bookings.exists():

                reply = """
                <strong>Your Booking Status:</strong>
                <br><br>
                """

                for booking in bookings:

                    if booking.room:

                        booking_name = (
                            f"Room {booking.room.room_name}"
                        )

                    elif booking.device:

                        booking_name = (
                            f"Device: {booking.device.device_name}"
                        )

                    else:

                        booking_name = "Booking"

                    status = booking.status.capitalize()

                    reply += f"""
                    • <strong>{booking_name}</strong>
                    <br>
                    Date: {booking.booking_date}
                    <br>
                    Status: <strong>{status}</strong>
                    <br><br>
                    """

            else:

                reply = """
                You do not have any bookings yet.
                """


    # ==========================================
    # PENDING BOOKINGS
    # ==========================================

    elif (
        'pending booking' in message
        or 'pending bookings' in message
        or 'my pending booking' in message
        or 'my pending bookings' in message
        or 'do i have any pending bookings' in message
        or 'what are my pending bookings' in message
        or 'รออนุมัติ' in message
        or 'การจองที่รออนุมัติ' in message
    ):

        if not request.user.is_authenticated:

            reply = """
            Please login first to view your pending bookings.
            """

        else:

            bookings = Booking.objects.filter(
                user=request.user,
                status='pending'
            ).order_by(
                '-booking_date',
                '-start_time'
            )

            if bookings.exists():

                reply = """
                <strong>Your Pending Bookings:</strong>
                <br><br>
                """

                for booking in bookings:

                    if booking.room:

                        booking_name = (
                            f"Room {booking.room.room_name}"
                        )

                    elif booking.device:

                        booking_name = (
                            f"Device: {booking.device.device_name}"
                        )

                    else:

                        booking_name = "Booking"

                    reply += f"""
                    • <strong>{booking_name}</strong>
                    <br>
                    Date: {booking.booking_date}
                    <br>
                    Time: {booking.start_time} - {booking.end_time}
                    <br>
                    Purpose: {booking.purpose}
                    <br>
                    Status: <strong>Pending</strong>
                    <br><br>
                    """

                reply += """
                Your booking is waiting for Admin approval.
                """

            else:

                reply = """
                You do not have any pending bookings.
                """


    # ==========================================
    # MY BOOKINGS
    # ==========================================

    elif (
        'my booking' in message
        or 'my bookings' in message
        or 'my reservation' in message
        or 'my reservations' in message
        or 'การจองของฉัน' in message
    ):

        if not request.user.is_authenticated:

            reply = """
            Please login first to view your bookings.
            """

        else:

            bookings = Booking.objects.filter(
                user=request.user
            ).order_by(
                '-booking_date',
                '-start_time'
            )

            if bookings.exists():

                reply = """
                <strong>My Bookings:</strong>
                <br><br>
                """

                for booking in bookings:

                    if booking.room:

                        booking_name = (
                            f"Room {booking.room.room_name}"
                        )

                    elif booking.device:

                        booking_name = (
                            f"Device: {booking.device.device_name}"
                        )

                    else:

                        booking_name = "No room"

                    reply += f"""
                    • <strong>{booking_name}</strong>
                    <br>
                    Date: {booking.booking_date}
                    <br>
                    Time: {booking.start_time} - {booking.end_time}
                    <br>
                    Purpose: {booking.purpose}
                    <br>
                    Status: <strong>{booking.status}</strong>
                    <br><br>
                    """

            else:

                reply = """
                You do not have any bookings yet.
                """


    # ==========================================
    # DEVICE BOOKING INSTRUCTIONS
    # ==========================================

    elif (
        'how do i book a device' in message
        or 'how can i book a device' in message
        or 'how to book a device' in message
        or 'book a device' in message
        or 'device booking' in message
        or 'วิธีจองอุปกรณ์' in message
        or 'จองอุปกรณ์' in message
    ):

        reply = """
        <strong>To book a device:</strong>

        <br><br>

        1. Go to <strong>Devices</strong>.
        <br>
        2. Select an available device.
        <br>
        3. Click <strong>Book</strong>.
        <br>
        4. Select the date and time.
        <br>
        5. Enter the purpose of booking.
        <br>
        6. Submit your booking request.

        <br><br>

        Your device booking will be waiting for
        <strong>Admin approval</strong>.
        """


    # ==========================================
    # ROOM BOOKING INSTRUCTIONS
    # ==========================================

    elif (
        'how do i book a room' in message
        or 'how can i book a room' in message
        or 'how to book a room' in message
        or 'วิธีจองห้อง' in message
        or 'จองห้อง' in message
        or 'book a room' in message
    ):

        reply = """
        <strong>To book a room:</strong>

        <br><br>

        1. Go to <strong>Rooms</strong>.
        <br>
        2. Select an available room.
        <br>
        3. Click <strong>Book</strong>.
        <br>
        4. Select the date and time.
        <br>
        5. Enter the purpose of booking.
        <br>
        6. Submit your booking request.

        <br><br>

        Your room booking will be waiting for
        <strong>Admin approval</strong>.
        """


    # ==========================================
    # GENERAL BOOKING
    # ==========================================

    elif (
        'book' in message
        or 'booking' in message
        or 'จอง' in message
    ):

        reply = """
        To book a room:

        <br><br>

        1. Go to <strong>Rooms</strong>.
        <br>
        2. Select an available room.
        <br>
        3. Click <strong>Book</strong>.
        <br>
        4. Select the date and time.
        <br>
        5. Enter the purpose of booking.
        <br>
        6. Submit your booking request.

        <br><br>

        Your booking will be waiting for
        <strong>Admin approval</strong>.
        """


    # ==========================================
    # DEFAULT
    # ==========================================

    else:

        reply = """
        I can help you with:

        <br>
        • Available rooms
        <br>
        • Available devices
        <br>
        • Room booking
        <br>
        • Device booking
        <br>
        • My bookings
        <br>
        • Pending bookings
        <br>
        • Booking status
        <br>
        • Specific room booking status

        <br><br>

        Try asking:
        <br>
        <strong>Which rooms are available?</strong>
        <br>
        <strong>What devices are available?</strong>
        <br>
        <strong>How do I book a device?</strong>
        <br>
        <strong>Show my pending bookings</strong>
        <br>
        <strong>
        What is the status of my room 203 booking?
        </strong>
        """

    return JsonResponse({
        'reply': reply
    })