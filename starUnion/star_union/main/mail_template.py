# we can make if as a factory in the coming deleveries
class otpMailTemplate:
    def __init__(self, otp):
        self.otp = otp
        self.logo = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"

    def getTemplate(self):
        return f"""
                <html>
                <head>
                    <title>Confirmation Email</title>
                </head>
                <body style="font-family: Arial, sans-serif; ">

                    <!-- Logo -->
                    <div style="text-align: center;">
                        <img src="{self.logo}" alt="Your Logo" style="max-width: 200px; border-radius:50%;
                        filter: drop-shadow(0 0 0.3rem #13022d);">
                    </div>

                    <!-- Main Content -->
                    <div style="margin: 20px;">
                        <h1 style="text-align: center;">Confirm to be a star 💫</h1>
                        <p style="text-align: center;">
                            Thank you for your interest! We're excited to have you join us.
                            Please click the button below to confirm your star status:
                        </p>

                        <!-- Confirmation Button -->
                        <div style="text-align: center; margin-top: 20px; color : red">
                            <p>Your Otp is: {self.otp}</p>
                        </div>
                    </div>

                </body>
            </html>
        """
