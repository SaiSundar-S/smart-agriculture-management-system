# from twilio.rest import Client
# import random
# from tkinter import *
# from tkinter import messagebox
# class otp_verifier(Tk):
#     def __init_(self):
#         super().__init__()
#         self.geometry("600x500")
#         self.resizable(False,False)
#         self.n=random.randint(1000,9000)
#         self.client=Client("","")
#         self.client.messages.create(to=[""],
#                                     from_="",
#                                     body=self.n)
        
#     def labels(self):
#         self.c=Canvas(self,bg="white",width=400,height=280)
#         self.c.place(x=100,y=60)
#         self.Login_Title=Label(self,text="OTP Verfication",font="bold ,20",bg="white")
#         self.Login_Title.place(x=210,y=90)
#     def Entry(self):
#         self.User_Name=Text(self,borderwidth=2,wrap="word",width=20,height=2)
#         self.User_Name.place(x=198,y=160)
       

#     def Buttons(self):
#         self.submitButtonImage=Label(self,text="submit",font="bold ,20",bg="orange")
#         self.submitButton=Button(self,image=self.submitButtonImage,command=self.checkOTP,border=0)
#         self.submitButton.place(x=200,y=400)
        
#         self.resendOTPImage=Label(self,text="submit",font="bold ,20",bg="orange")
#         self.resendOTP=Button(self,image=self.resendOTPImage,command=self.resendOTPOTP,border=0)
#         self.resendOTP.place(x=200,y=400)
#     def resendotp(self):
#         self.n=random.randint(1000,9000)
#         self.client=Client("","")
#         self.client.messages.create(to=[""],
#                                     from_="",
#                                     body=self.n)
        
        
# if __name__=="__main__":
#     window=otp_verifier()
#     window.mainloop()