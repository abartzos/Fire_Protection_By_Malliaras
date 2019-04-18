class MultiDKNN():
    def __init__(self):
        self.x = [[]]
        self.y = []
        self.dimensions = 0
        
    def check_iterable(self,obj):
        '''Returns true if an objeck is iterable otherwise it return false. Meant for internal use'''
        try:
            obj[0]
            return True
        except:
            return False
    
    def check(self):
        '''Checks that the training data provide is of the correct type and shape. Meant for internal use'''
        if self.check_iterable(self.y) != True: #check that labels are in a list
            raise TypeError("The labels must be contained in a list-like object")
        if self.check_iterable(self.x) != True:
            raise TypeError("The features must be in a list-like object")
        if len(self.x) != len(self.y):
            raise Exception("The list-like object of features must be the same lenght as the list-like object of labels")
        
        for i in self.x:
            if self.check_iterable(i) != True:
                raise TypeError("The coordinates of each point must be in a list-like object")
        
        self.dimensions = len(self.x[0]) #find how many coordinates the points have
        
        for i in self.x: #check that all points have the same num of coordinates
            if len(i) != self.dimensions:
                raise Exception("All points need to have the same number of coordinates")    
        
    def fit(self,x,y): #x must be a list of lists(coordinates(features)), y must be a list(labels) 
        '''
        Fits the model. Takes two arguments: 
            x: Must be list-like object of list-like objects containing the features  
            y: Must be a list-like object containing the labels for each point
        ''' 
        self.x = x
        self.y = y
        self.check()
        
    def find_distance(self,i,j):
        '''Returns the distance of two n-dimensional vertices. Meant for internal use by the classifier'''
        s = 0
        for dimension in range(self.dimensions):
            s = s + (i[dimension] - j[dimension])**2
        distance = s**0.5
        return(distance)
    
    def argsort(self,l):
        '''Returns a list-like object containing the sorted indexes of a list-like object.Meant for internal use'''  
        sorted_list = sorted(l)
        sorted_indexes = []
        for el in sorted_list:
            sorted_indexes.append(l.index(el))
        return sorted_indexes
    
    def mode(self,l):
        '''Returns the mode(most common element) of a list-like object. Meant for internal use'''
        counter = {}
        most_common_element = 0
        most_common_element_vote = 0
        for i in l:
            if i not in counter:
                c = 0
                for e in l:
                    if e == i:
                        c += 1
            counter[i] = c
        for i in counter:
            if counter[i] > most_common_element_vote:
                most_common_element = i
                most_common_element_vote = counter[i]
        return most_common_element    
        
    def predict(self,p,k):
        '''
        Predicts the label of a new point or points. Takes 2 arguments:
            p: Unlabeled point/points must be a list-like object that either containes floating point values (for one point) or 
                list-like objects containing floating point values (for many points, each list represents a point)
            k: The number of nearest neighbors the classifier takes into consideration. Must be an integer
        '''
        if self.check_iterable(p) == True:
            if self.check_iterable(p[0]) != True:
                distances = []
                smallest_distances_indexes = []
                possible_labels = []
                for i in self.x:
                    distance = self.find_distance(p,i)
                    distances.append(distance)
                smallest_distances_indexes = self.argsort(distances)
                for i in smallest_distances_indexes[:k]:
                    possible_labels.append(self.y[i])   
                return self.mode(possible_labels)
            else:
                outcomes = []
                for point in p:
                    outcomes.append(self.predict(point,k))
                return outcomes
        else:
            raise TypeError("The coordinates of the unlabeled point/points must be in a list or other list-like object")
    
    def score(self,predicted_labels,true_labels):
        '''
        Returns a value for 0.0 to 1.0 which represents the accuracy of the classifier's results, the bigger the value the more accurate the classifier. 
        Takes 2 arguments:
            predicted_labels: A list-like object that contains the results of a classifier for a specific set of points. 
                              Use labeled points in the MultiDKNN().predict() to get those 
            true_labels: A list-like object that contains the valid labels of a specific set of points
        '''
            
        i = 0
        num_of_corrects = 0
        for label in predicted_labels:
            if label == true_labels[i]:
                num_of_corrects += 1
            i += 1
        return num_of_corrects/len(predicted_labels)
    
    def optimizek(self,p,true_labels,up_limit):
        '''
        Returns the optimal value of k for a specific dataset. Takes 3 arguments:
            p:unlabeled point/points must be a list-like object that either containes floating point values (for one point) or 
                list-like objects containing floating point values (for many points, each list represents a point)  
            true_labels: the label or labels for p. Must be a list-like object of equal lenght with p
            up_limit: The highest value of k to be examined. All values from 1 to up_limit(contained) will be checked. Must be an integer
        '''
        optimal_k = (0,0)
        for i in range(1,up_limit+1):
            outcomes = self.predict(p,i)
            current_accuracy = self.score(outcomes,true_labels)
            if current_accuracy > optimal_k[1]:
                optimal_k = (i,current_accuracy)
            if current_accuracy == 1.0:
                break
        return optimal_k[0]