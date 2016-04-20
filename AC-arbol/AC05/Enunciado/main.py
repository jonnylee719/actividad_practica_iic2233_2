# coding=utf-8

# Recuerda borrar los 'pass'. Pudes borrar si quieres los comentarios.


class Commit:
    id = 0
    def __init__(self, message, changes,id_commit_padre=None):
        self.message = message
        self.changes = changes
        self.id_commit= Commit.id
        Commit.id +=1
        self.id_commit_padre=id_commit_padre
        self.hijos={}
        #self.branches= None

    def agregar_hijo(self,nuevo_hijo):
        if self.id == nuevo_hijo.id:
            self.message = nuevo_hijo.message
            self.changes = nuevo_hijo.changes
        else:
            self.hijos.update(nuevo_hijo)


    def encontrar_ultimo_hijo(self):
        if self.hijos is None:
            return self.hijos
        else:





class Branch:

    #############
    # COMPLETAR:
    # Crear __init__ con lo que consideres necesario
    #############
    def __init__(self,name):
        self.name = name
        self.primer_commit = None
        self.new_branches = dict

    def new_commit(self, commit):
        if self.primer_commit is None:
            self.primer_commit = commit
        else:
            self.primer_commit.agregar_hijo(commit)


        #############
        # COMPLETAR:
        # Agregar un nuevo commit del tipo Commit a esta branch.
        # Este commit define el estado final temporalmente.
        #############

        #self.primer_commit.eencontrar_ultimo_hijo()

    def pull(self):
        files = []
        #############
        # COMPLETAR:
        # Retornar el estado final de esta branch (una lista de archivos).
        #############
        return files


class Repository:

    def __init__(self, name):
        self.name = name
        self.branches = [Branch("master")]
        #############
        # COMPLETAR:
        # Crear branch 'master'.
        # Crear commit inicial y agregarlo a 'master'.
        #############

    def create_branch(self, new_branch_name, from_branch_name):
        #############
        # COMPLETAR:
        # Crear branch a partir del último estado de la 'from_branch_name'.
        from_branch = self.branch(from_branch_name)
        from_branch_primer_commit = from_branch.primer_commit
        ultimo_commit = from_branch_primer_commit.encontrar_ultimo_hijo()
        ultimo_commit.agregar_hijo()
        """
        from_branch = self.branch(from_branch_name)
        from_branch_primer_commit = from_branch.primer_commit
        ultimo_commit = from_branch_primer_commit.encontrar_ultimo_hijo()
        nuevo_branch = Branch(str(new_branch_name)
        nuevo_branch.new_commit(ultimo_commit)
        self.branches.append(nuevo_branch)
        from_branch.new_branches[]=
        """
        pass

    def branch(self, branch_name):
        #############
        # COMPLETAR:
        # Retornar la branch con el nombre 'branch_name'.
        #############
        for a in self.branches:
            if a.name == branch_name:
                return a

    def checkout(self, commit_id):
        files = []
        #############
        # COMPLETAR:
        # Buscar el commit con cierta id y retornar el estado del repositorio
        # hasta ese commit. Puede estar en cualquier branch.
        #############
        return files


if __name__ == '__main__':
    # Ejemplo de uso
    # Puedes modificarlo para probar esto pero al momento de la corrección
    # el ayudante borrará cualquier cambio y restaurará las siguientes lineas
    # a su estado original (como se muestran aquí).

    repo = Repository("syllabus 2.0")

    repo.branch("master").new_commit(Commit(
        message="agregado readme",
        changes=[("CREATE", "README.md")]
    ))

    repo.branch("master").new_commit(Commit(
        message="archivos base",
        changes=[("CREATE", "main.py"), ("CREATE", "clases.py")]
    ))

    # Creamos una rama del estado actual de 'master'
    repo.create_branch("desarrollo-de-vistas", 'master')
    repo.branch("desarrollo-de-vistas").new_commit(Commit(
        message="imagenes",
        changes=[("CREATE", "main.jpg"), ("CREATE", "user.png")]
    ))

    repo.branch("desarrollo-de-vistas").new_commit(Commit(
        message="cambiar instrucciones",
        changes=[("DELETE", "README.md"), ("CREATE", "instrucciones.html")]
    ))

    repo.branch("master").new_commit(Commit(
        message="datos recolectados",
        changes=[("CREATE", "data.csv")]
    ))

    print(repo.branch("master").pull())
    # Esperamos que el repo esté así:
    # ['.jit', 'README.md', 'main.py', 'clases.py', 'data.csv']

    print(repo.branch("desarrollo-de-vistas").pull())
    # Esperamos que el repo esté así:
    # ['.jit', 'main.py', 'clases.py',
    #  'main.jpg', 'user.png', 'instrucciones.html']

    print(repo.checkout(4))
    # Esperamos que el repo esté así:
    # ['.jit', 'README.md', 'main.py', 'clases.py', 'main.jpg', 'user.png']

    print(repo.checkout(1))
    # Esperamos que el repo esté así:
    # ['.jit']