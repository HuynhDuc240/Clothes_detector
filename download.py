from google_images_download import google_images_download  
import sys
import pandas as pd
import re
# creating object 
response = google_images_download.googleimagesdownload()  

search_queries = [ 
'shirt black formal','shirt white formal','shirt red formal','shirt yellow formal','shirt gray formal','shirt blue formal','shirt green',
'Tshirt black','Tshirt white','Tshirt red','Tshirt yellow','Tshirt gray','Tshirt blue','Tshirt green',
'coat black','coat white','coat red','coat yellow','coat gray','coat blue','coat green'
] 


def downloadimages(query): 
    # keywords is the search query 
    # format is the image file format 
    # limit is the number of images to be downloaded 
    # print urs is to print the image file url 
    # size is the image size which can 
    # be specified manually ("large, medium, icon") 
    # aspect ratio denotes the height width ratio 
    # of images to download. ("tall, square, wide, panoramic") 
    arguments = {"keywords": query, 
                 "print_urls":True,
                 "limit":100, 
                } 
    try: 
        response.download(arguments) 
      
    # Handling File NotFound Error     
    except FileNotFoundError:  
        arguments = {"keywords": query,  
                     "limit":100, 
                     "print_urls":True,  
                    } 
                       
        # Providing arguments for the searched query 
        try: 
            # Downloading the photos based 
            # on the given arguments 
            response.download(arguments)  
        except: 
            pass
  
# Driver Code 
for query in search_queries: 
    info = re.split(r'\s',query)
    orig_stdout = sys.stdout
    f = open('URLs.txt','w')
    sys.stdout = f
    #####download####
    downloadimages(query)  
    sys.stdout = orig_stdout
    f.close()

    with open('URLs.txt') as f:
        content = f.readlines()
    f.close()

    data = pd.DataFrame(columns=['type','color','url'])
    for j in range(len(content)):
        if content[j][:9] == 'Completed':
            temp = {'type':[info[0]],'color':[info[1]],'url':[content[j-1][11:-1]]}
            d = pd.DataFrame(data=temp)
            data = data.append(d)
    fileName = info[0]+"_"+info[1]+".csv"
    data.to_csv(fileName,sep="\t",index=False)
    