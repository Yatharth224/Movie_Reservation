# 🎬 Movie Reservation System (OTP Based)

## 📌 Project Overview
The **Movie Reservation System** is a simple and user-friendly web application that allows users to book movie tickets **without online payment**.

This system is specially designed for users who **do not trust online payments** or feel insecure about payment failures.  
Instead of payment, bookings are confirmed using an **OTP (One Time Password)** system.

---

## ⭐ Key Features

### 🔐 Login & Signup
- User authentication system
- Secure login and signup
- Only logged-in users can book seats

---

### 🎥 Movie Dashboard
- List of available movies
- Movie details (show time, venue, seats)
- Real-time seat availability

---

---

### ⏳ Seat Hold System (5 Minutes)
- When a user selects a seat:
  - The seat is **held for 5 minutes**
  - During this time, **no other user can book that seat**
- If the user does not complete the booking within 5 minutes:
  - The seat is **automatically released**

✅ Prevents unfair blocking of seats

---

### 🔑 OTP-Based Booking (No Payment Required)
- ❌ No online payment required
- ✅ Booking is confirmed using OTP
- OTP is used as booking verification

This system is ideal for users who:
- Avoid online payments
- Are worried about payment failures

---

### 📖 My Bookings
- Users can view their **previous bookings**
- Shows movie name, venue, time, and seat details
- Booking history is securely stored
