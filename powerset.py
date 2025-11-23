#create a powerset of a string(all combinations of the characters in teh string)
# abc = a, b, c, ab, ac, bc, abc, ""



def powerset(str):

    resultSet = []
    def build_combo(build, depth):
        if depth == len(str):
            resultSet.append(build)
            return resultSet
        build_combo(build + str[depth], depth+1)
        build_combo(build, depth+1)

    build_combo("",0)
    return resultSet



  #           abc
  #       /         \

  # ab    ac


print(powerset("abc"))
