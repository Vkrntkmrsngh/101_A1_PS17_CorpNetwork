import sys

sys.stdout = open("outputPS17.txt", "w")
class Node():

    def __init__(self, node_label, type):
        self.node = node_label
        self.type = type


    def __eq__(self, other):
        return self.node == other.node

    def __str__(self):
        return self.node


class CorporateNetwork():
    DirectorCompany = []  # list of Node Objects containing companies and directors
    edges = []  # matrix of edges/ associations

    def printAdjList(self):

        print("*****************Graph Adjacency List**********************")

        for graph_node in self.DirectorCompany:
            indx = self.DirectorCompany.index(graph_node)
            print("{}-> {}".format(graph_node.node, self.edges[indx]))

    def getAdjacencyList(self, node):

        try :
            input_node= Node(node, "")
            indx = self.DirectorCompany.index(input_node)
            return set(self.edges[indx])
        except ValueError as e :
            print("Error : Node {} does not exist in the graph".format(node))

    def displayAll(self):

        print("********************DISPLAY ALL**************************")
        totalcomp = 0
        totaldirectors = 0
        companyList = []
        directorList = []

        if (len(self.DirectorCompany) == 0):
            print("The graph is empty")
        else:
            for graph_node in self.DirectorCompany:
                if (graph_node.type == "Company"):
                    totalcomp = totalcomp + 1
                    companyList.append(graph_node.node)
                else:
                    totaldirectors = totaldirectors + 1
                    directorList.append(graph_node.node)

            print("Total no. of Companies:{}".format(totalcomp))
            print("Total no. of Directors:{}".format(totaldirectors))
            print("List of Companies:")
        print(*companyList, sep="\n")
        print("List of Directors:")
        print(*directorList, sep="\n")

    def displayCompanies(self, Director):

        print("*****************DISPLAY COMPANIES**************************")

        try :
            director_node = Node(Director.upper(), "Director")
            indx = self.DirectorCompany.index(director_node)
            if(self.DirectorCompany[indx].type == "Director"):
                print("Director name:{}".format(Director))
                print("List of Companies:")
                print(*self.edges[indx], sep="\n")
            else:
                print("Error: Input Director : {} is not a director node in the graph".format(Director))
        except ValueError as e :
            print("Error : Director {} does not exist in the graph".format(Director))

    def displayDirectors(self, Company):

        print("*****************DISPLAY DIRECTORS**************************")

        try :
            comp_node= Node(Company.upper(), "Company")
            indx = self.DirectorCompany.index(comp_node)
            if (self.DirectorCompany[indx].type == "Company"):
                print("Company name:{}".format(Company))
                print("List of Directors:")
                print(*self.edges[indx], sep="\n")
            else:
                print("Error: Input Company : {} is not a company node in the graph".format(Company))
        except ValueError as e :
            print("Error : Company {} does not exist in the graph".format(Company))




    def findCommonDirector(self, CompanyA, CompanyB):

        print("*****************FIND COMMON DIRECTORS**************************")

        print("Company A:{}".format(CompanyA))
        print("Company B:{}".format(CompanyB))
        try :
            compAindx = self.DirectorCompany.index(Node(CompanyA.upper(), "Company"))
            compBindx = self.DirectorCompany.index(Node(CompanyB.upper(), "Company"))
            common_direcor_list = []

            if(self.DirectorCompany[compAindx].type == "Company" and self.DirectorCompany[compBindx].type == "Company"):

                for director in self.edges[compAindx]:

                    if(director in self.edges[compBindx]):
                        common_direcor_list.append(director)


                if (len(common_direcor_list) > 0):
                    print("Related: Yes,{}".format(*common_direcor_list),sep=":")
                else:
                    print("Companies {} and {} have no common directors".format(CompanyA,CompanyB))
            else:
                print("Error: Either CompanyA:{} or CompanyB:{} is not a company node in the graph".format(CompanyA,CompanyB))
        except ValueError as e :
                print("Error : CompanyA:{} or CompanyB:{} does not exist in the graph".format(CompanyA,CompanyB))



    def bfs(self,startNode,endNode):

        visited_node = []
        to_visit_node = []

        # Start with Company A
        to_visit_node.append(startNode)
        visited_node.append(startNode)

        while (len(to_visit_node) > 0):

            s = to_visit_node.pop(0)
            adj_list = self.getAdjacencyList(s)

            for curr_node in adj_list:
                if (curr_node not in visited_node):
                    if (curr_node == endNode):
                        return True
                    visited_node.append(curr_node)
                    to_visit_node.append(curr_node)

        return False


    def findRelatedCompany(self, CompanyA, CompanyB):

        print("*****************FIND RELATED COMPANY**************************")

        print("Company A:{}".format(CompanyA))
        print("Company B:{}".format(CompanyB))

        try :
            compAindx = self.DirectorCompany.index(Node(CompanyA.upper(), "Company"))
            compBindx = self.DirectorCompany.index(Node(CompanyB.upper(), "Company"))

            if (self.DirectorCompany[compAindx].type == "Company" and self.DirectorCompany[compBindx].type == "Company"):
                res = self.bfs(CompanyA.upper(), CompanyB.upper())
                if (res):
                    print("Related:Yes")
                else:
                    print("Related:No")
            else:
                print("Error: Either CompanyA:{} or CompanyB:{} is not a company node in the graph".format(CompanyA, CompanyB))

        except ValueError as e :
                print("Error : CompanyA:{} or CompanyB:{} does not exist in the graph".format(CompanyA,CompanyB))


    def readCompanyDirfile(self, inputfile):
        with open(inputfile, 'r') as fp:
            lines = fp.readlines()
            for line in lines:
                inputList = line.rstrip('\n').split(" / ")
                comp_name = inputList[0].rstrip(" ").upper()
                comp_node = Node(comp_name,"Company")
                try:
                    indx = self.DirectorCompany.index(comp_node)
                    self.edges[indx].append([director.upper() for director in inputList[1:]])
                except ValueError as e:
                    self.DirectorCompany.append(comp_node)
                    indx = len(self.DirectorCompany) - 1
                    self.edges.insert(indx, [director.upper() for director in inputList[1:]])

                for director in inputList[1:]:
                    director_node = Node(director.rstrip(" ").upper(), "Director")
                    try:
                        indx = self.DirectorCompany.index(director_node)
                        self.edges[indx].append(comp_name)
                    except ValueError as e:
                        self.DirectorCompany.append(director_node)
                        indx = len(self.DirectorCompany) - 1
                        self.edges.insert(indx, [comp_name])


if __name__ == '__main__':
    corp = CorporateNetwork()
    corp.readCompanyDirfile('inputPS17.txt')
    #corp.printAdjList()
    corp.displayAll()

    with open("promptsPS17.txt", 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            func_to_run = line.rstrip('\n').split(":")[0].rstrip(" ").lstrip(" ")

            if(func_to_run == "findCompany"):
                director_name = line.rstrip('\n').split(":")[1].rstrip(" ").lstrip(" ")
                corp.displayCompanies(director_name)
            elif(func_to_run == "listDirectors"):
                company_name = line.rstrip('\n').split(":")[1].rstrip(" ").lstrip(" ")
                corp.displayDirectors(company_name)
            elif(func_to_run == "CommonDirector"):
                companyA_name = line.rstrip('\n').split(":")[1].rstrip(" ").lstrip(" ")
                companyB_name = line.rstrip('\n').split(":")[2].rstrip(" ").lstrip(" ")
                corp.findCommonDirector(companyA_name,companyB_name)
            elif (func_to_run == "RelatedCompany"):
                companyA_name = line.rstrip('\n').split(":")[1].rstrip(" ").lstrip(" ")
                companyB_name = line.rstrip('\n').split(":")[2].rstrip(" ").lstrip(" ")
                corp.findRelatedCompany(companyA_name,companyB_name)
            else:
                print("Error: Invalid input")



