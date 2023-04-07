import socketserver
from pymongo import MongoClient
import json
import sys
import base64
import hashlib

mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
chat_collection = db["chat"]
comments_collection = db["comments"]
chat_id_collection = db["chat_id"]

def get_next_id():
    id_object = chat_id_collection.find_one({})
    if id_object:
        next_id = int(id_object['last_id']) + 1
        chat_id_collection.update_one({}, {'$set': {'last_id': next_id}})
        return next_id
    else:
        chat_id_collection.insert_one({'last_id': 1})
        return 1
    
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(2048)
        print(received_data)
        sys.stderr.flush()
        sys.stdout.flush()

        string1 = received_data
        splitline = string1.split(b"\r\n\r\n", 1)
        splitline2 = splitline[0].decode().split("\r\n")
        #print("Split2:", splitline2)
        splitline3 = splitline2[0].split(" ")

        path = splitline3[1]
        print("Path" ,path)
        requestType = splitline3[0]

        body = splitline[1]
         # get content length, length of body in bytes, compare. Request missing bytes, add to body


    #splitting headers

        headers = splitline[0]

        splitheaders = headers.split(b"\r\n")

        splitheaders = splitheaders[1:]

        #print(splitheaders)
        headersDi = {}

        for i in splitheaders:
            value = i.split(b":", 1)
            #print(value)
            v = value[1].decode()
            val = v.strip()
            headersDi[value[0]] = (val).encode()

        cont_length = headersDi.get(b"Content-Length",b'0')
        cn_len = cont_length.decode()

        while(len(body) < int(cn_len)):
            body += self.request.recv(min(2048, int(cn_len) - len(body)))

        #print(body)

        #print(headersDi)




        indexFile = open("index.html", "rb").read()
        lenIndexFile = str(len(indexFile))

        cssFile = open("style.css", "rb").read()
        lenCssFile = str(len(cssFile))

        jsFile = open("functions.js", "rb").read()
        lenJsFile = str(len(jsFile))

        imageFlam = open("image/flamingo.jpg", "rb").read()
        lenImageFlam = str(len(imageFlam))

        imageCat = open("image/cat.jpg", "rb").read()
        lenImageCat = str(len(imageCat))

        imageDog = open("image/dog.jpg", "rb").read()
        lenImageDog = str(len(imageDog))

        imageEagle = open("image/eagle.jpg", "rb").read()
        lenImageEagle = str(len(imageEagle))

        imageElephant = open("image/elephant.jpg", "rb").read()
        lenImageElephant = str(len(imageElephant))

        imageKitten = open("image/kitten.jpg", "rb").read()
        lenImageKitten = str(len(imageKitten))

        imageParrot = open("image/parrot.jpg", "rb").read()
        lenImageParrot = str(len(imageParrot))

        imageRabbit = open("image/rabbit.jpg", "rb").read()
        lenImageRabbit = str(len(imageRabbit))

        if(requestType == "GET"):
            if(path == "/hello"):
                self.request.sendall("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n X-Content-Type-Options: nosniff\r\nContent-Length: 7\r\n\r\nWhatsup".encode())
            elif(path == "/hi"):
                self.request.sendall("HTTP/1.1 301 Permanently Moved\r\nContent-Length: 0\r\n X-content-Type-Options: nosniff\r\nLocation: /hello\r\n\r\n".encode())
            elif(path == "/"):
                #if comment exists in the database edit html using python
                com = (comments_collection.find({}, {"_id": 0}))
                
                listedCom = list(com)

                #print("com", com)
                #print("type of com",type(com))
                #print("listedCom", listedCom)
                #print("type of listedCom", type(listedCom))
                # if listedCom:
                    
                
                xfiles = open("index.html", "rb")
                htmlFile = xfiles.read()
                xfiles.close()

                stringCom = b""
                stringImage = b""
                #imagePlaceholder = b""

                for x in listedCom:
                    var = x["Comment"]
                    var = var.replace(b"&", b"&amp;")
                    var = var.replace(b"<", b"&lt;")
                    var = var.replace(b">", b"&gt;")
                    stringCom += b"<p>" + var + b"</p>"
                    var1 = x.get("Image", None)
                    if var1:
                        byteVar = var1.encode()
                        print("TYPEVARBYTE: ", type(byteVar))
                        print("byteVar: ", byteVar)
                        print("Type var1", type(var1))
                        if byteVar == b'/':
                            self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                        
                        stringCom += b'<img src="' + byteVar + b'" class="my_image"/>'
                    

                commentIn = htmlFile.find(b'{{content}}')
                oldComment = htmlFile[commentIn:commentIn+11]

                #print("StringCom is", stringCom)

                newFile = htmlFile.replace(oldComment, stringCom)

                lenHtmlFile = len(newFile)


                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\ncharset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(lenHtmlFile) + "\r\n\r\n").encode() + newFile)   

            elif(path == "/style.css"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\ncharset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenCssFile + "\r\n\r\n").encode() + cssFile)
            elif(path == "/functions.js"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\ncharset=utf-8\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenJsFile + "\r\n\r\n").encode() + jsFile)
            elif(path == "/image/flamingo.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageFlam + "\r\n\r\n").encode() + imageFlam)
            elif(path == "/image/cat.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageCat + "\r\n\r\n").encode() + imageCat)
            elif(path == "/image/dog.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageDog + "\r\n\r\n").encode() + imageDog)
            elif(path == "/image/eagle.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageEagle + "\r\n\r\n").encode() + imageEagle)
            elif(path == "/image/elephant.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageElephant + "\r\n\r\n").encode() + imageElephant)
            elif(path == "/image/kitten.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg;\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageKitten + "\r\n\r\n").encode() + imageKitten)
            elif(path == "/image/parrot.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageParrot + "\r\n\r\n").encode() + imageParrot)
            elif(path == "/image/rabbit.jpg"):
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + lenImageRabbit + "\r\n\r\n").encode() + imageRabbit)
            elif(path == "/users"):
                a = json.dumps(list(chat_collection.find({}, {"_id": 0})))
                aLen = str(len(a))
                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + aLen + "\r\n\r\n").encode() + a.encode())
            elif(path == "/websocket"):
                print("Headers: ", headersDi)
                ke = received_data.find(b'Sec-WebSocket-Key')
                print("ke", ke)

                print("vindex BF:", received_data[ke:])
                vindex = received_data[ke+19:]
                vinSplit = vindex.split(b"\r\n")
                print("Vindex", vindex)
                print("vinSPlit", vinSplit)
                daKey = vinSplit[0]
                print("dakey", daKey)
                daKey += b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

                print("dakey", daKey)

                hashShaKey = hashlib.sha1(daKey).hexdigest()
                print("HASH", hashShaKey)
                keyB64 = base64.b64encode(bytes.fromhex(hashShaKey)).decode()

                print(keyB64)

                self.request.sendall(("HTTP/1.1 101 Switching Protocols\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Accept: " + (keyB64) + "\r\n\r\n").encode())       

                while True:
                    pass

            elif("/file" in path):
                path = path.replace("/", "")
                path = "uploads/" + path

                image1 = open(path, "rb").read()
                #print(image1)
                lenImage1 = str(len(image1))

                self.request.sendall(("HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(lenImage1) + "\r\n\r\n").encode() + image1)
            else:
                self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        elif(requestType == "POST"):

            if(path == "/users"):
                bodyDetails = json.loads(body)

                bodyDetails["id"] = get_next_id()

                userID = bodyDetails["id"]

                chat_collection.insert_one(bodyDetails)

                bodyDetailz = json.dumps(chat_collection.find_one({"id": userID}, {"_id": 0}))

                self.request.sendall(("HTTP/1.1 201 OK\r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\n\r\n").encode() + bodyDetailz.encode())
            if(path == "/image-upload"):
                #print(body)
                type1 = headersDi[b"Content-Type"]

                #if length of recdata is < content length header
                type1 = type1.replace(b"multipart/form-data; boundary=", b"--") + b"\r\n"
                type2 = type1.replace(b"multipart/form-data; boundary=", b"--") + b"--\r\n"
                
                bodySplit = body.split(type1)

                bodySplitz = bodySplit[1].split(b"\r\n\r\n", 1)
                imSplitz = bodySplit[2].split(b"\r\n\r\n", 1)

                #print("BodySplitz", bodySplitz)
                #print("body", body)

                print("ImSplitz", imSplitz)
                
                if b"Content-Type: image/jpeg" in imSplitz[0]:
                    imageSplitz = imSplitz[1].strip(type2)
                    print("ImageSplitz", imageSplitz)
                else:
                    imageSplitz = b""

                #print("IMAGESPLITZ", imageSplitz)
                
                actualComment = bodySplitz[1]

                newID = get_next_id()

                f = open("uploads/file" + str(newID) + ".jpg", "wb+")
                f.write(imageSplitz)
                f.close()

                filename = "file" + str(newID) + ".jpg"

                commentDic = {}
                commentDic["Comment"] = actualComment
                if imageSplitz != b"":
                    commentDic["Image"] = filename

                comments_collection.insert_one(commentDic)
                print(commentDic)

                self.request.sendall("HTTP/1.1 301 Permanently Moved\r\nContent-Length: 0\r\nX-content-Type-Options: nosniff\r\nLocation: /\r\n\r\n".encode())
        else:
            self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                                           
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    server = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    server.serve_forever()






