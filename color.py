from __future__ import division


class catColor:
    
    def __init__(self, **kwargs):
        s = [i for i in range(0, kwargs['setLevel'])]
        self.catDivider = kwargs['levelDiv']
        self.setDict = {}
        self.permList = []
        for x in s:
    		self.permList.append([x])
    	for l in range(2, 4):
    		ls = []
    		for i in self.permList:
    			for x in s:
    				k = i + [x]
    				ls.append(k)
    		self.permList = ls
        for i in range(0, len(self.permList)):
            key = str(tuple(self.permList[i]))
            self.setDict[key] = 's' + str(i)
        
    def cat(self, color):
        d = self.catDivider;
        r = color[0] // d; g = color[1] // d; b = color[2] // d; 
        return self.setDict[str((r, g, b))]
    
    def revCat(self, color_set):
        set_no = int(color_set[1:])
        color_tuple = [x * self.catDivider for x in self.permList[set_no]]
        return color_tuple
        #return [x * self.catDivider for x in color_tuple]
        
        
        
if __name__ == "__main__":
    c = catColor(setLevel = 8, levelDiv = 32)
    print c.revCat('s146')
    print c.revCat('s219')
    print c.revCat('s292')
    print c.revCat('s438')
    print c.revCat('s73')
        