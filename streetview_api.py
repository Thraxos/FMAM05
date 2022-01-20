# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 00:03:56 2021
@author: Marcus
"""

import requests
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import numpy as np

class StreetViewer(object):
    def __init__(self, api_key, location, pic_folder_directory, meta_folder_directory, header_folder_directory, size="640x640", verbose=True):
        """
        This class handles a single API request to the Google Static Street View API
        api_key: obtain it from your Google Cloud Platform console
        location: the address string or a (lat, lng) tuple
        size: returned picture size. maximum is 640*640
        pic_folder_directory: directory to save the returned picture from request
        meta_folder_directory: directory to save the returned meta data from request
        header_folder_directory: directory to save the returned header from request
        verbose: whether to print the processing status of the request
        """
        # input params are saved as attributes for later reference
        self._key = api_key
        self.location = location
        self.size = size
        self.pic_folder_directory = pic_folder_directory
        self.meta_folder_directory = meta_folder_directory
        self.header_folder_directory = header_folder_directory
        # call params are saved as internal params
        self._meta_params = dict(key=self._key, location=self.location)
        self._pic_params = dict(key=self._key, location=self.location, size=self.size)
        self.verbose = verbose
        

    def get_meta(self):
        """
        Method to query the metadata of the address
        """
        # saving the metadata as json for later usage
        # "/"s are removed to avoid confusion on directory
        self.meta_path = "{}meta{}.json".format(self.meta_folder_directory, self.location.replace("/", ""))
        self._meta_response = requests.get('https://maps.googleapis.com/maps/api/streetview/metadata?', params=self._meta_params)
        # turning the contents as meta_info attribute
        self.meta_info = self._meta_response.json()
        # meta_status attribute is used in get_pic method to avoid
        # query when no picture will be available
        self.meta_status = self.meta_info['status']
        if self._meta_response.ok:
            if self.verbose:
                print(">>> Obtained Meta from StreetView API:")
                print(self.meta_info)
            with open(self.meta_path,'w') as file:
                json.dump(self.meta_info, file)
        else:
            print(">>> Failed to obtain Meta from StreetView API!!!")
                
        self._meta_response.close()
        
    def get_pic(self):
        """
        Method to query the StreetView picture and save to local directory
        """
        # define path to save picture and headers
        self.pic_path = "{}pic_{}".format(self.pic_folder_directory, self.location.replace("/", ""))
        self.header_path = "{}header_{}.json".format(self.header_folder_directory, self.location.replace("/", ""))
        # only when meta_status is OK will the code run to query picture (cost incurred)
        if self.meta_status == 'OK':
            if self.verbose:
                print(">>> Picture available, requesting now...")
            self._pic_response = requests.get('https://maps.googleapis.com/maps/api/streetview?', params=self._pic_params)
            self.pic_header = dict(self._pic_response.headers)
            if self._pic_response.ok:
                if self.verbose:
                    print(f">>> Saving objects to {self.pic_folder_directory}")
                with open(self.pic_path, 'wb') as file:
                    file.write(self._pic_response.content)
                with open(self.header_path, 'w') as file:
                    json.dump(self.pic_header, file)
                self._pic_response.close()
                if self.verbose:
                    print(">>> COMPLETE!")
        else:
            print(">>> Picture not available in StreetView, ABORTING!")
        
    def display_pic(self):
        """
        Method to display the downloaded street view picture if available
        """
        if self.meta_status == 'OK':
            plt.figure(figsize = (10, 10))
            img = mpimg.imread(self.pic_path)
            imgplot = plt.imshow(img)
            plt.show()
        else:
            print(">>> Picture not available in StreetView, ABORTING!")

# with open('basement.csv', newline='') as f:
#     reader = csv.reader(f)
#     non_basement_list = list(reader)
    
# for i in range(np.size(non_basement_list)):
#     gwu_viewer = StreetViewer(api_key ='AIzaSyCj8XSRmPrkDZNJxL8t3UDn3U9GSEa1lv4',
#                             location = str(non_basement_list[i][0]) + ', MALMÖ.jpg',
#                             pic_folder_directory='./basement streetviews/',
#                             meta_folder_directory='./basement streetviews metadata/',
#                             header_folder_directory='./basement streetviews headers/',
#                             size = "256x256", 
#                             verbose = False)
#     gwu_viewer.get_meta()
#     gwu_viewer.get_pic()
    

# with open('non basement.csv', newline='') as f:
#     reader = csv.reader(f)
#     non_basement_list = list(reader)
    
# for i in range(np.size(non_basement_list)):
#     gwu_viewer = StreetViewer(api_key ='AIzaSyCj8XSRmPrkDZNJxL8t3UDn3U9GSEa1lv4',
#                             location = str(non_basement_list[i][0]) + ', MALMÖ.jpg',
#                             pic_folder_directory='./non basement streetviews/',
#                             meta_folder_directory='./non basement streetviews metadata/',
#                             header_folder_directory='./non basement streetviews headers/',
#                             size = "256x256", 
#                             verbose = False)
#     gwu_viewer.get_meta()
#     gwu_viewer.get_pic()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        