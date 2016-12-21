#/usr/lib/phantomjs
# coding=utf-8 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from color import catColor
driver = webdriver.PhantomJS("/usr/lib/phantomjs/phantomjs", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        
class css_prop:
    
    def __init__(self, url, fn, option):
        self.option = option
        self.driver = driver;
        self.attr_list = []
        self.color_set = set()
        self.id_count = 0
        self.driver.get(url)
        root = self.driver.find_element_by_tag_name("body")
        if fn == 'recDfs':
            self.result = self.recDfs(root, self.gen_id())
        elif fn == 'iterBfs':
            self.result = self.iterBfs(root)
        
    #---------------------------------------------#
    #function to get next-immediate child elements
    def find_child_elements(self,elem):
        try:
            return elem.find_elements_by_xpath("./*")
        except Exception, e:
            return []
    
    #---------------------------------------------#
    #function to generate id for elements
    def gen_id(self):
    
        elem_id = "elem" + str(self.id_count)
        self.id_count += 1
    
        return elem_id
    
    #---------------------------------------------#
    #function to convert unicode rgba string to rgb int arry
    def rgb_int(self, rgba_u):
        rgbaStr = str(rgba_u).replace("rgba(", "").replace(")", "").replace(" ", "").split(",");
        rgbInt = tuple([int(rgbaStr[i]) for i in range(0, 3)])
        return rgbInt
        
    #---------------------------------------------#
    #function to generate attribute json
    def attr_json(self,elem):
        tag_name = elem.tag_name
        class_name = elem.get_attribute("class")
        id_attr = elem.get_attribute("id")
        bgColor = self.rgb_int(elem.value_of_css_property("background-color"))
        textColor = self.rgb_int(elem.value_of_css_property("color"))
        borderColor = elem.value_of_css_property("border-color")
        width = elem.value_of_css_property("width")
        height = elem.value_of_css_property("height")
    
        return {"id": "", "tag": tag_name, "class": class_name, "id_attr": id_attr, "bgColor": bgColor, "textColor": textColor, "borderColor": borderColor, "width": width, "height": height, "children": []}
    
    #---------------------------------------------#
    #function to traverse dom
    #and update information about the elements 
    def recDfs(self, elem, elem_id):
        
        if(self.option == "both" or self.option == "allCss"):
            json = self.attr_json(elem)
            json["id"] = elem_id
        if(self.option == "both" or self.option == "colorOnly"):
            bg_color = self.rgb_int(elem.value_of_css_property("background-color"))
            text_color = self.rgb_int(elem.value_of_css_property("color"))
            self.color_set.add(bg_color)
            self.color_set.add(text_color)
        
        children = self.find_child_elements(elem)
        if not children:
            return
        else:
            for child in children:
                if child.tag_name not in ["script", "style"]:
                    
                    child_id = self.gen_id()
                    if(self.option == "both" or self.option == "allCss"):
                        json["children"].append(child_id)
                        self.attr_list.append(json)
                        
                    self.recDfs(child, child_id)
            
            
        return { "attr": self.attr_list, "color": self.color_set }
    
    #---------------------------------------------#
    #update color values in color_set
    def appendColor(self, elem):
        bg_color = self.rgb_int(elem.value_of_css_property("background-color"))
        text_color = self.rgb_int(elem.value_of_css_property("color"))
        self.color_set.add(bg_color)
        self.color_set.add(text_color)
                
    #---------------------------------------------#
    #function to traverse dom
    def iterBfs(self, root):
        self.appendColor(root)
        children = self.find_child_elements(root)
        level = 1;
        while children and level<=25:
            next_children = []
            for child in children:
                if child.tag_name not in ["script", "style"]:
                    self.appendColor(child)
                    grandChildren = self.find_child_elements(child)
                    for x in grandChildren:
                        next_children.append(x)
            children = next_children
            level += 1;
        return { 'color': self.color_set, 'level': level }
        
    #---------------------------------------------#
    #main function which is used to collect all required data from a site       
    def collect(self):
        return self.result["color"];
        
    def level(self):
        return self.result["level"];
        
    def getPage(self):
        return self.driver.page_source;
    
        
if __name__ == "__main__":
    #--------------TESTING-----------------#
    cato = catColor(setLevel = 8, levelDiv = 32)
    
    sites = [
        'http://xtnote.com'
        ]
    
    '''
    sites = [
        'https://www.youtube.com',
        'http://www.w3schools.com',
        'https://thecravity.com',
        'http://www.havaki.com',
        'https://www.kaggle.com',
        'https://www.google.com',
        'https://c9.io'
        ]
    '''
    
    for i in sites:
        print "Started crawling ==> ", i
        crawler = css_prop(i, 'iterBfs', "colorOnly")
        color = crawler.collect()
        print "-------------------------"    
        print "unique-colors Set"
        print "-------------------------"    
        for i in color:
            print i, '==>', cato.cat(i)