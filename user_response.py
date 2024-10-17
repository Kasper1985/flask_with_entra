class UserInfoResponse:
    def __init__(self, odata_context, businessPhones, displayName, givenName, jobTitle, mail, mobilePhone, officeLocation, preferredLanguage, surname, userPrincipalName, id):
        self.odata_context = odata_context
        self.businessPhones = businessPhones
        self.displayName = displayName
        self.givenName = givenName
        self.jobTitle = jobTitle
        self.mail = mail
        self.mobilePhone = mobilePhone
        self.officeLocation = officeLocation
        self.preferredLanguage = preferredLanguage
        self.surname = surname
        self.userPrincipalName = userPrincipalName
        self.id = id

    def __str__(self):
        return "\n".join(key + ": " + str(value) for key, value in self.__dict__.items())

    @staticmethod
    def from_dict(obj: any) -> 'UserInfoResponse':
        assert isinstance(obj, dict)
        odata_context = obj.get("@odata.context")
        businessPhones = obj.get("businessPhones")
        displayName = obj.get("displayName")
        givenName = obj.get("givenName")
        jobTitle = obj.get("jobTitle")
        mail = obj.get("mail")
        mobilePhone = obj.get("mobilePhone")
        officeLocation = obj.get("officeLocation")
        preferredLanguage = obj.get("preferredLanguage")
        surname = obj.get("surname")
        userPrincipalName = obj.get("userPrincipalName")
        id = obj.get("id")
        return UserInfoResponse(odata_context, businessPhones, displayName, givenName, jobTitle, mail, mobilePhone, officeLocation, preferredLanguage, surname, userPrincipalName, id)