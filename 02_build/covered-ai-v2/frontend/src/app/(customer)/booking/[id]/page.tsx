/**
 * Customer App - Booking Confirmation Page
 * 
 * Shown after Gemma books an appointment.
 * Reassures customer their booking is confirmed.
 */

"use client";

import React from "react";
import { Calendar, Clock, MapPin, Phone, MessageSquare, CheckCircle } from "lucide-react";

// Mock data - in production, loaded from URL params or API
const mockBooking = {
  business: {
    name: "Titan Plumbing",
    phone: "+447712345678",
    logo: null, // URL to logo
  },
  booking: {
    id: "BK-2024-001",
    date: "Monday, 2nd December",
    time: "9:00am - 11:00am",
    job: "Tap repair",
    address: "14 Park Road, NE3 4AB",
    engineer: "Ralph",
  },
  customer: {
    name: "Mrs Chen",
  },
};

export default function BookingConfirmationPage() {
  const { business, booking, customer } = mockBooking;
  
  return (
    <div className="px-5 py-8">
      {/* Business header */}
      <div className="text-center mb-8">
        {business.logo ? (
          <img 
            src={business.logo} 
            alt={business.name}
            className="h-12 mx-auto mb-2"
          />
        ) : (
          <h1 className="text-xl font-bold text-neutral-900">{business.name}</h1>
        )}
      </div>
      
      {/* Confirmation */}
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <CheckCircle className="w-8 h-8 text-green-600" />
        </div>
        <h2 className="text-2xl font-bold text-neutral-900 mb-2">
          Booking Confirmed
        </h2>
        <p className="text-neutral-600">
          Hi {customer.name.split(" ")[1] || customer.name}, your appointment is booked.
        </p>
      </div>
      
      {/* Booking details */}
      <div className="bg-neutral-50 rounded-2xl p-5 mb-6">
        <h3 className="font-semibold text-neutral-900 mb-4">{booking.job}</h3>
        
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <Calendar className="w-5 h-5 text-neutral-400" />
            <span className="text-neutral-700">{booking.date}</span>
          </div>
          <div className="flex items-center gap-3">
            <Clock className="w-5 h-5 text-neutral-400" />
            <span className="text-neutral-700">{booking.time}</span>
          </div>
          <div className="flex items-center gap-3">
            <MapPin className="w-5 h-5 text-neutral-400" />
            <span className="text-neutral-700">{booking.address}</span>
          </div>
        </div>
        
        <p className="text-sm text-neutral-500 mt-4">
          {booking.engineer} will be with you. We'll text you when they're on the way.
        </p>
      </div>
      
      {/* Actions */}
      <div className="space-y-3">
        <a
          href={`tel:${business.phone}`}
          className="flex items-center justify-center gap-2 w-full py-4 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-colors"
        >
          <Phone className="w-5 h-5" />
          Call to Change Booking
        </a>
        
        <a
          href={`sms:${business.phone}`}
          className="flex items-center justify-center gap-2 w-full py-4 bg-neutral-100 text-neutral-700 font-semibold rounded-xl hover:bg-neutral-200 transition-colors"
        >
          <MessageSquare className="w-5 h-5" />
          Send a Message
        </a>
      </div>
      
      {/* Add to calendar */}
      <div className="mt-8 text-center">
        <button className="text-blue-600 text-sm font-medium">
          Add to Calendar
        </button>
      </div>
      
      {/* Booking reference */}
      <p className="text-center text-xs text-neutral-400 mt-8">
        Booking ref: {booking.id}
      </p>
    </div>
  );
}
