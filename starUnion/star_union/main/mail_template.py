# we can make if as a factory in the coming deleveries
class otpMailTemplate:
    def __init__(self, otp, logo):
        self.otp = otp
        self.logo = logo

    def getTemplate(self):
        return f"""
                <html>
                <head>
                    <title>Confirmation Email</title>
                </head>
                <body style="font-family: Arial, sans-serif; ">
                    <center>
                        <!-- Logo -->
                        <div style="text-align: center;">
                            <img src="{self.logo}" alt="Your Logo" style="max-width: 13vw; border-radius:50%;
                            filter: drop-shadow(0 0 0.5rem #13022d); ">
                        </div>

                        <!-- Main Content -->
                        <div style=" font-size: 1rem; font-weight: bold; margin-top:1rem">
                            <h1 style="text-align: center; margin: 0">Confirm to be a star 💫</h1>
                            <!-- Confirmation Button -->
                            <div style="text-align: center; color : rgba(97, 56, 209, 1)">
                                <p >Your Otp is: {self.otp}</p>
                            </div>
                        </div>
                    </center>
                </body>
            </html>
        """
