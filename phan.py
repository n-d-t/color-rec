#/usr/lib/phantomjs
# coding=utf-8 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from color import catColor


class css_prop:
    
    def __init__(self,url,option):
        self.option = option;
        self.attr_list = []
        self.color_set = set()
        self.id_count = 0
        self.driver = webdriver.PhantomJS("/usr/lib/phantomjs/phantomjs", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        self.driver.get(url)
        root = self.driver.find_element_by_tag_name("body")
        self.result = self.dfs(root, self.gen_id())
        
    #---------------------------------------------#
    #function to get next-immediate child elements
    def find_child_elements(self,elem):
        return elem.find_elements_by_xpath("./*")
    
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
    def dfs(self, elem, elem_id):
        
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
                        
                    self.dfs(child, child_id)
            
            
        return { "attr": self.attr_list, "color": self.color_set }
                
                
    #---------------------------------------------#
    #main function which is used to collect all required data from a site       
    def collect(self):
        return self.result
    
    def __del__(self):
        self.driver.close()
        print "destory"
        
if __name__ == "__main__":
    for i in ["http://www.google.com","http://www.xtnote.com","http://www.fast.com"]:
        #--------------TESTING-----------------#
        crawler = css_prop("http://www.google.com","colorOnly")
        print crawler.result;
        cato = catColor(setLevel = 8, levelDiv = 32)
        #setLevel - how many level are there in each R, G and B values
        #levelDiv - by which value you've to floor divided the R, G, and B values,
        #           so that you can divide them into different levels
        
        val = crawler.collect();
        #val = crawler.collect("http://w3schools.com", "colorOnly")
        
        #call collect fn with three option:
        #   1: allCss       - to get all css attributes with context
        #   2: colorOnly    - to get set of unique colors used in the web page
        #   3: both         - to get both the above mentioned result sets
        
        prop = val['attr']
        color = val['color']
        
        #if the collect fn is called with 'colorOnly', then val['attr'] will be empty
        #if the collect fn is called with 'allCss', then val['color'] will be empty
        
        print "-------------------------"    
        print "unique-colors Set"
        print "-------------------------"    
        for i in color:
            print i, '==>', cato.cat(i)
        