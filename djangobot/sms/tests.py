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
        self.assertEqual(aReturn[1], "Would you like a SMALL, MEDIUM, or LARGE?", "welcome message line 2")
        self.assertEqual(aReturn[2], "SMALL is $5, MEDIUM is $9, LARGE is $15", "welcome message line 3")
        self.assertEqual(oOrder.getState(), "SIZE", "order state should be SIZE")
    def test_size(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("small")
        self.assertEqual(aReturn[0], "What toppings would you like?", "size message line 1")
        self.assertEqual(aReturn[1], "Please enter a list with commas", "size message line 2")
        self.assertEqual(aReturn[2], "+$2 per each topping")
        self.assertEqual(oOrder.getState(), "TOPPINGS", "order state should be TOPPINGS")
        self.assertEqual(oOrder.getSize(), "small", "size should be small")
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("medium")
        self.assertEqual(aReturn[0], "What toppings would you like?", "size message line 1")
        self.assertEqual(aReturn[1], "Please enter a list with commas", "size message line 2")
        self.assertEqual(aReturn[2], "+$2 per each topping")
        self.assertEqual(oOrder.getState(), "TOPPINGS", "order state should be TOPPINGS")
        self.assertEqual(oOrder.getSize(), "medium", "size should be small")
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("large")
        self.assertEqual(aReturn[0], "What toppings would you like?", "size message line 1")
        self.assertEqual(aReturn[1], "Please enter a list with commas", "size message line 2")
        self.assertEqual(aReturn[2], "+$2 per each topping")
        self.assertEqual(oOrder.getState(), "TOPPINGS", "order state should be TOPPINGS")
        self.assertEqual(oOrder.getSize(), "large", "size should be small")
    def test_toppings(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"TOPPINGS"})
        aReturn = oOrder.handleInput("blueberry, apple, lemon")
        self.assertEqual(aReturn[0], "Would you like drinks with that?", "toppings message line 1")
        self.assertEqual(aReturn[1], "Please enter a list with commas or NO", "toppings message line 2")
        self.assertEqual(aReturn[2], "+$2 per each drink", "price for toppings")
        self.assertEqual(oOrder.getState(), "DRINKS", "order state should be DRINKS")
        self.assertEqual(oOrder.getToppings(), "blueberry, apple, lemon", "toppings should be as entered")
    def test_no_drinks(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("medium")
        aReturn = oOrder.handleInput("blueberry, apple, lemon")
        aReturn = oOrder.handleInput("no")
        self.assertEqual(aReturn[0], "Thank you for your order", "drinks message line 1")
        self.assertEqual(aReturn[1], "medium pie with blueberry, apple, lemon", "complete order")
        self.assertEqual(aReturn[2], "Please pick up in 20 minutes", "drinks message line 2")
        self.assertEqual(aReturn[3], "The price is $15", "price for the order")
        self.assertEqual(oOrder.getState(), "DONE", "order state should be DONE")
        self.assertEqual(oOrder.getDrinks(), None, "no drinks were entered")
    def test_drinks(self):
        oOrder = Order(phone = '123-456-7890', data={"state":"SIZE"})
        aReturn = oOrder.handleInput("medium")
        aReturn = oOrder.handleInput("blueberry, apple, lemon")
        aReturn = oOrder.handleInput("dr.pepper")
        self.assertEqual(aReturn[0], "Thank you for your order", "drinks message line 1")
        self.assertEqual(aReturn[1], "medium pie with blueberry, apple, lemon", "complete order")
        self.assertEqual(aReturn[2], "dr.pepper", "drink option")
        self.assertEqual(aReturn[3], "Please pick up in 20 minutes", "drinks message line 2")
        self.assertEqual(aReturn[4], "The price is $17", "price for the order")
        self.assertEqual(oOrder.getState(), "DONE", "order state should be DONE")
        self.assertEqual(oOrder.getDrinks(), "dr.pepper", "no drinks were entered")