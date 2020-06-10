import boto3
import time
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n"),
        ("¿",""),
        ("?",""),
        (".",""),
        (",",""),
        ("-",""),
        ("\\n",""),
        (" ",""),
        ("¡",""),
        ("!",""),
        ("'",""),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def read_str(bucket,name):
    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':name}})
    textDetections=response['TextDetections']
    Words=[]
    for text in textDetections:
        if (text['Type']=='WORD'):
            palabra=normalize(text['DetectedText'].lower())
            Words.append(palabra)
    return Words
if __name__ == "__main__":

    bucket='pruebas601'
    control='control.png'

    client=boto3.client('rekognition')
    file1 = open("log.txt","a") 
  
    response_control=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':control}})

                        
    textDetections=response_control['TextDetections']
    Words=[]
    #print (textDetections)
    #print ('Matching faces')
    for text in textDetections:
        #print ('Type:' + text['Type'])
        if (text['Type']=='WORD'):    
            print ('Detected text:' + text['DetectedText'])
            palabra=normalize(text['DetectedText'].lower())
            if (float("{:.2f}".format(text['Confidence']))>95):
                Words.append(palabra)
            print ("IT'S" in text['DetectedText'])
            #print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            #print ('Id: {}'.format(text['Id']))
            #if 'ParentId' in text:
                #print ('Parent Id: {}'.format(text['ParentId']))
            
            #print
    print (Words)
    
    #prueba_name=input("nombre de la prueba:")
    prueba_name='control.png'
    while (prueba_name!='0'):
        prueba=read_str(bucket,prueba_name)
        print (prueba)
        con=0
        for i in prueba:
            if (i in Words):
                con=con+1
        porcentage=con/len(prueba)
        print ('total=', con/len(prueba))
        if (porcentage==1.0):
            line="Nombre de prueba:"+prueba_name+" Resultado: true\n"+"Fecha de prueba: "+str(time.asctime( time.localtime(time.time()) ))+"\n"
            line=line+" Se encontró un "+str(porcentage)+" de palabras de la prueba en la imagen de control\n"
            file1.write(line)

        else:
            line="Nombre de prueba:"+prueba_name+" Resultado: false\n"+"Fecha de prueba: "+str(time.asctime( time.localtime(time.time()) ))+"\n"
            line=line+"Se encontró un "+str(porcentage)+" de palabras de la prueba en la imagen de control\n"
            file1.write(line)
        prueba_name=input("nombre de la prueba:")

    file1.close()
        



    
