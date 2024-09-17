# Définition

Un [commutateur empilable](https://fr.wikipedia.org/wiki/Commutateur_empilable) (*stackable switch* ou *stack switch*) est un commutateur réseau qui est complètement fonctionnel pris isolément, mais qui peut également être préparé pour coopérer avec un ou plusieurs autres commutateurs de façon à n'en former qu'un seul logique.

**Avantages :** 
- permet d'améliorer la fiabilité et la flexibilité du réseau ; 
- permet d'augmenter la bande-passante ;
- évite aux utilisateurs de gérer plusieurs appareils en même temps, en particulier dans les centres de données ou les salles informatiques de taille moyenne ;
- permet un changement dynamique (ajout ou retrait de commutateur dans la pile (*stack*)) sans affecter les performances ou la stabilité du réseau ;
- si un lien échoue dans la pile, les autres switches ne cesseront pas de fonctionner.

# Infrastructure 

Bases :
- les switches doivent être de la même "gamme" et du même fournisseur, avec le même niveau de firmware
- les switches doivent être reliés par des câbles DAC (*Direct Attach Copper*) type SPF QSPF, des émetteurs-récepteurs optiques ou des câbles d'empilages spécialisés.

Ces switches fonctionneront comme s'ils n'étaient qu'un, partageront la même configuration et la même adresse IP, ainsi que la même console de configuration.

Deux rôles fondamentaux : 
- switch *master* - switch central qui gère tous les autres, effectue une configuration et une gestion unifiée sur tous les autres switches. S'il tombe en panne, un autre switch de la pile est désigné *master*.
- switches *slaves* - généralement tous les autres switches de la pile.

## Topologie 

Il existe deux topologies typiques de connexion de piles : 
- topologie en chaîne 
- topologie en anneau 

**Topologie en chaîne** : 
- le premier et le dernier membre de la pile n'ont pas besoin d'être reliés : convient à un empilage sur une distance relativement longue ; 
- cependant, si un membre de la pile échoue, la pile se divise.
**Topologie en anneau :**
- lorsqu'un des maillons de la pile tombe en panne, la topologie devient une topologie en chaîne et la pile continue de fonctionner normalement ; 
- cependant, le premier et le dernier membre de la pile doivent être reliés, ce qui n'est pas forcément adapté à de la transmission à longue distance lorsque la topologie est empilée avec des câbles DAC à courte portée.

