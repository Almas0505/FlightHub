"""
Email service for sending notifications
"""
import logging
from typing import Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', '1025'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@flighthub.com')
        
    def send_email(self, to_email: str, subject: str, html_body: str):
        """
        Send email
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_body: HTML body
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_user and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                
                server.send_message(msg)
            
            logger.info(f"Email sent to {to_email}: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}", exc_info=True)
    
    def send_booking_confirmation(self, booking_data: Dict[str, Any]):
        """Send booking confirmation email"""
        to_email = booking_data.get('contact_email')
        pnr = booking_data.get('pnr')
        
        subject = f"Booking Confirmation - {pnr}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #2196F3;">Booking Confirmed!</h2>
            <p>Dear Customer,</p>
            <p>Your booking has been confirmed. Here are the details:</p>
            
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Booking Reference (PNR):</strong> {pnr}</p>
                <p><strong>Flight Number:</strong> {booking_data.get('flight_number')}</p>
                <p><strong>Route:</strong> {booking_data.get('departure_airport')} → {booking_data.get('arrival_airport')}</p>
                <p><strong>Departure:</strong> {booking_data.get('departure_time')}</p>
                <p><strong>Total Amount:</strong> {booking_data.get('total_amount')} {booking_data.get('currency', 'USD')}</p>
            </div>
            
            <p>Please complete your payment to confirm your reservation.</p>
            <p>Payment expires in 15 minutes.</p>
            
            <p style="margin-top: 30px;">Thank you for choosing FlightHub!</p>
            <p style="color: #666; font-size: 12px;">This is an automated email. Please do not reply.</p>
        </body>
        </html>
        """
        
        self.send_email(to_email, subject, html_body)
    
    def send_ticket(self, booking_data: Dict[str, Any]):
        """Send e-ticket email"""
        to_email = booking_data.get('contact_email')
        pnr = booking_data.get('pnr')
        
        subject = f"E-Ticket - {pnr}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #4CAF50;">E-Ticket Issued!</h2>
            <p>Dear Customer,</p>
            <p>Your e-ticket has been issued successfully.</p>
            
            <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Booking Reference (PNR):</strong> {pnr}</p>
                <p><strong>Flight Number:</strong> {booking_data.get('flight_number')}</p>
                <p><strong>Status:</strong> ✅ Ticketed</p>
            </div>
            
            <p>Please arrive at the airport at least 2 hours before departure.</p>
            <p>You can check-in online 24 hours before your flight.</p>
            
            <p style="margin-top: 30px;">Have a great flight!</p>
            <p style="color: #666; font-size: 12px;">This is an automated email. Please do not reply.</p>
        </body>
        </html>
        """
        
        self.send_email(to_email, subject, html_body)
    
    def send_booking_cancellation(self, booking_data: Dict[str, Any]):
        """Send booking cancellation email"""
        to_email = booking_data.get('contact_email')
        pnr = booking_data.get('pnr')
        
        subject = f"Booking Cancelled - {pnr}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #f44336;">Booking Cancelled</h2>
            <p>Dear Customer,</p>
            <p>Your booking has been cancelled.</p>
            
            <div style="background: #ffebee; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Booking Reference (PNR):</strong> {pnr}</p>
                <p><strong>Status:</strong> ❌ Cancelled</p>
            </div>
            
            <p>If you paid for this booking, a refund will be processed within 5-7 business days.</p>
            
            <p style="margin-top: 30px;">We hope to serve you again soon!</p>
            <p style="color: #666; font-size: 12px;">This is an automated email. Please do not reply.</p>
        </body>
        </html>
        """
        
        self.send_email(to_email, subject, html_body)
    
    def send_flight_reminder(self, booking_data: Dict[str, Any]):
        """Send flight reminder 24h before departure"""
        to_email = booking_data.get('contact_email')
        pnr = booking_data.get('pnr')
        
        subject = f"Flight Reminder - {pnr}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #FF9800;">Flight Reminder</h2>
            <p>Dear Customer,</p>
            <p>This is a reminder that your flight is in 24 hours.</p>
            
            <div style="background: #fff3e0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Booking Reference (PNR):</strong> {pnr}</p>
                <p><strong>Flight Number:</strong> {booking_data.get('flight_number')}</p>
                <p><strong>Departure:</strong> {booking_data.get('departure_time')}</p>
            </div>
            
            <p><strong>Checklist:</strong></p>
            <ul>
                <li>✓ Check-in online (if not done)</li>
                <li>✓ Print or download boarding pass</li>
                <li>✓ Check baggage allowance</li>
                <li>✓ Arrive 2 hours early</li>
            </ul>
            
            <p style="margin-top: 30px;">Have a safe flight!</p>
            <p style="color: #666; font-size: 12px;">This is an automated email. Please do not reply.</p>
        </body>
        </html>
        """
        
        self.send_email(to_email, subject, html_body)
    
    def send_payment_confirmation(self, payment_data: Dict[str, Any]):
        """Send payment confirmation email"""
        to_email = payment_data.get('payer_email')
        payment_id = payment_data.get('payment_id')
        
        subject = f"Payment Confirmation - {payment_id}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #4CAF50;">Payment Successful!</h2>
            <p>Dear Customer,</p>
            <p>Your payment has been processed successfully.</p>
            
            <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Payment ID:</strong> {payment_id}</p>
                <p><strong>Amount:</strong> {payment_data.get('amount')} {payment_data.get('currency')}</p>
                <p><strong>Status:</strong> ✅ Completed</p>
            </div>
            
            <p>You will receive your e-ticket shortly.</p>
            
            <p style="margin-top: 30px;">Thank you for your payment!</p>
            <p style="color: #666; font-size: 12px;">This is an automated email. Please do not reply.</p>
        </body>
        </html>
        """
        
        self.send_email(to_email, subject, html_body)
    
    def send_payment_failure(self, payment_data: Dict[str, Any]):
        """Send payment failure email"""
        to_email = payment_data.get('payer_email')
        payment_id = payment_data.get('payment_id')
        
        subject = f"Payment Failed - {payment_id}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #f44336;">Payment Failed</h2>
            <p>Dear Customer,</p>
            <p>Unfortunately, your payment could not be processed.</p>
            
            <div style="background: #ffebee; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Payment ID:</strong> {payment_id}</p>
                <p><strong>Amount:</strong> {payment_data.get('amount')} {payment_data.get('currency')}</p>
                <p><strong>Status:</strong> ❌ Failed</p>
            </div>
            
            <p>Please try again or use a different payment method.</p>
            <p>If the problem persists, contact your bank or our support team.</p>
            
            <p style="margin-top: 30px;">We're here to help!</p>
            <p style="color: #666; font-size: 12px;">This is an automated email. Please do not reply.</p>
        </body>
        </html>
        """
        
        self.send_email(to_email, subject, html_body)
