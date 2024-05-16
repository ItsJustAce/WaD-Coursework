def calculate_booking_price(city_price, booking_date, today_date):
  """
  Calculates the booking price considering city pricing and discount based on booking date.

  Args:
      city_price (float): Base price for the booking based on the city.
      booking_date (datetime.date): Date of the booking.
      today_date (datetime.date): Today's date.

  Returns:
      float: Final booking price after applying discount (if any).
  """

  # Calculate the number of days in advance
  days_in_advance = (booking_date - today_date).days

  # Apply discount based on number of days in advance
  if days_in_advance >= 80:
    discount = 0.3  # 30% discount
  elif days_in_advance >= 60:
    discount = 0.2  # 20% discount
  elif days_in_advance >= 45:
    discount = 0.1  # 10% discount
  else:
    discount = 0  # No discount

  # Calculate final price with discount
  final_price = city_price * (1 - discount)

  return final_price