# Desafio Intelie
### The Hitchhikers Guide to Facts and Schema

A solução web encontra-se hospedada na plataforma em nuvem Heroku. Para acessá-la, basta utilizar o link: [Facts and Schema](https://facts-and-schema.herokuapp.com/). 
No caso de não funcionamento da plataforma por motivos adversos, uma solução é utilizar a versão do código que encontra-se no [Github](https://github.com/rodolphorosa/desafio-intelie). 
Nesse caso, após clonar o código, é necessário abrir o terminal, direcioná-lo para a pasta raiz do código, executar o comando python app.py e acessar o endereço: localhost:5000. 
Na ausência das bibliotecas Flask, lxml e MarkupSafe, será necessária a criação de um ambiente virtual para que a solução possa ser executada em sua máquina. 
Nesse caso, deve-se executar os seguintes comandos no Linux (no diretório do projeto):

    $ virtualenv -p python3 envname
    $ source envname/bin/activate
    $ pip install -r requirements.txt
    $ python app.py

Para testar apenas a funcionalidade destinada à resolução do problema de encontrar fatos vigentes, 
é necessário unicamente executar o módulo _schemaFacts.py_ utilizando o comando ```python schemaFacts.py``` na linha do comando do Windows/Linux. 


Ao abrir a página web da solução, será necessário realizar log in. 
Há dois usuários registrados: user e visitor, ambos com senha password. 
O primeiro tem como role “admin”, enquanto o segundo, “visitor”. 
Dessa forma, user terá acesso a todas as funcionalidades do sistema, ao passo que visitor terá acesso apenas às funcionalidades de visualização.  
Após efetuar login, o usuário é direcionado para a página principal da aplicação, que apresenta a lista de todos os fatos existentes. 
Na parte superior, estão disponíveis as opções Log out, Home, See Schema, See Current Facts, nessa ordem. 
Ao acessar See Schema, o usuário terá acesso à lista de atributos dos dados e as opções de adição, atualização e deleção de atributos. 
De forma análoga, ao acessar, See Current Facts, abrir-se-á uma página contendo todos os fatos vigentes; ao usuário serão oferecidas as opções de adicionar e deletar um fato. 
Ao clicar no nome de qualquer uma das entidades listadas, o usuário será direcionado para uma página onde é mostrado o histórico de manipulações realizada naquela entidades, isto é, as adições de novos atributos e deleção de um fato a ela associado. 
Ao realizar log out, o usuário é direcionado imediatamente para a tela de log in.
