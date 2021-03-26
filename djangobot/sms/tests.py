from django.test import TestCase
import sqlite3

# Create your tests here.

from sms.models import Order


class SMSTests(TestCase):
    def test_for_json_support(self):
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT JSON(\'{"a": "b"}\')')
            self.assertIs(False, False)
        except:
            self.assertIs(True, False, "no support for json in sqlite3")
    def test_welcome(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"WELCOMING"})
        aReturn = oOrder.handleInput("hello")
        self.assertEqual(aReturn[0], "Welcome to Wesley's pie shop", "welcome message line 1")
        self.assertEqual(aReturn[1], "Would you like a SMALL, or LARGE?", "welcome message line 2")
        self.assertEqual(aReturn[2], "SMALL is $5, LARGE is $15", "welcome message line 3")
        self.assertEqual(oOrder.getState(), "SIZE", "order state should be SIZE")
    def test_small(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("small")
        self.assertEqual(aReturn[0], "So far your order comes to $5", "price of small size")
        self.assertEqual(aReturn[1], "What toppings would you like?", "size message line 1")
        self.assertEqual(aReturn[2], "Please enter a list with commas", "size message line 2")
        self.assertEqual(aReturn[3], "+$2 per each topping")
        self.assertEqual(oOrder.getState(), "TOPPINGS", "order state should be TOPPINGS")
        self.assertEqual(oOrder.getSize(), "small", "size should be small")
        self.assertEqual(oOrder.getPrice(), 5, "price should be $5")
    def test_large(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("large")
        self.assertEqual(aReturn[0], "So far your order comes to $15", "price of large size")
        self.assertEqual(aReturn[1], "What toppings would you like?", "size message line 1")
        self.assertEqual(aReturn[2], "Please enter a list with commas", "size message line 2")
        self.assertEqual(aReturn[3], "+$2 per each topping")
        self.assertEqual(oOrder.getState(), "TOPPINGS", "order state should be TOPPINGS")
        self.assertEqual(oOrder.getSize(), "large", "size should be large")
        self.assertEqual(oOrder.getPrice(), 15, "price should be $5")
    def test_gigantic(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("gigantic")
        self.assertEqual(aReturn[0], "Oops we only have small and large", "size message line 1")
        self.assertEqual(aReturn[1], "Please enter small or large", "size message line 2")
        self.assertEqual(oOrder.getState(), "SIZE", "order state should be SIZE")
    
    def test_no_drinks(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("small")
        aReturn = oOrder.handleInput("blueberry, apple, lemon")
        aReturn = oOrder.handleInput("no")
        self.assertEqual(aReturn[0], "Thank you for your order", "drinks message line 1")
        self.assertEqual(aReturn[1], "small pie with blueberry, apple, lemon", "complete order")
        self.assertEqual(aReturn[2], "Please pick up in 20 minutes", "drinks message line 2")
        self.assertEqual(aReturn[3], "The price is $11", "price for the order")
        self.assertEqual(oOrder.getState(), "DONE", "order state should be DONE")
        self.assertEqual(oOrder.getDrinks(), None, "no drinks were entered")
    def test_drinks(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("small")
        aReturn = oOrder.handleInput("blueberry, apple, lemon")
        aReturn = oOrder.handleInput("dr.pepper")
        self.assertEqual(aReturn[0], "Thank you for your order", "drinks message line 1")
        self.assertEqual(aReturn[1], "small pie with blueberry, apple, lemon", "complete order")
        self.assertEqual(aReturn[2], "dr.pepper", "drink option")
        self.assertEqual(aReturn[3], "Please pick up in 20 minutes", "drinks message line 2")
        self.assertEqual(aReturn[4], "The price is $13", "price for the order")
        self.assertEqual(oOrder.getState(), "DONE", "order state should be DONE")
        self.assertEqual(oOrder.getDrinks(), "dr.pepper", "one drinks were entered")