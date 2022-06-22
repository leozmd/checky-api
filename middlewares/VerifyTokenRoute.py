from fastapi import Request
from auth.JWTFunctions import validateToken
from fastapi.routing import APIRoute


class VerifyTokenRoute(APIRoute):
    def getRouteHandler(self):
        originalRoute = super().getRouteHandler()

        async def verifyTokenMiddleware(request: Request):
            token = request.headers["Authorization"].split(" ")[1]
            validationResponse = validateToken(token, output=False)
            if validationResponse == None:
                return await originalRoute(request)
            else:
                return validationResponse
        return verifyTokenMiddleware
