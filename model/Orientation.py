class Orientation:

    def right(self, orientation):
        """ Dispatch method """
        method_name = 'right_' + orientation
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid orientation")
        # Call the method as we return it
        return method()

    def left(self, orientation):
        """ Dispatch method """
        method_name = 'left_' + orientation
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid orientation")
        # Call the method as we return it
        return method()

    def right_W(self):
        return 'N'

    def right_N(self):
        return 'E'

    def right_E(self):
        return 'S'

    def right_S(self):
        return 'W'

    def left_W(self):
        return 'S'

    def left_N(self):
        return 'W'

    def left_E(self):
        return 'N'

    def left_S(self):
        return 'E'