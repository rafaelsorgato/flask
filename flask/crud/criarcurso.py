from util import bd

mysql = bd.SQL("root", "123456", "tarefaatual")

comando = "DROP TABLE IF EXISTS tb_curso;"

if mysql.executar(comando, ()):
   print ("Tabela de cursos excluída com sucesso!")


comando = "create table tb_curso(" + \
          "idt_curso int not null auto_increment primary key," + \
          "sigla_curso char(10)," + \
          "nme_curso varchar(50)," + \
          "dta_curso date," + \
          "num_creditos int," + \
          "ementa text);"

if mysql.executar(comando, ()):
   print ("Tabela de cursos criada com sucesso!")