Title: Delegation: composition and inheritance in object-oriented programming
Date: 2020-08-17 09:00:00 +0100
Category: Programming
Tags: OOP, Python, Python3
Authors: Leonardo Giordani
Image: delegation-composition-and-inheritance-in-object-oriented-programming
Slug: delegation-composition-and-inheritance-in-object-oriented-programming
Summary: 

## Introduction

Object-oriented programming (OOP) is a methodology that was introduced in the 60s, though as for many other concepts related to programming languages it is difficult to give a proper date. While recent years have witnessed a second youth of functional languages, object-oriented is still a widespread paradigm among successful programming languages, and for good reasons. OOP is not the panacea for all the architectural problems in software development, but if used correctly can give a solid foundation to any system.

It might sound obvious, but if you use an object-oriented language or a language with strong OOP traits, you have to learn this paradigm well. Being very active in the Python community, I see how many times young programmers are introduced to the language, the main features, and the most important libraries and frameworks, _without a proper and detailed description of OOP and how OOP is implemented in the language_.

The _implementation_ part is particularly important, as OOP is a set of concepts and features that are expressed theoretically and then implemented in the language, with specific traits or choices. It is very important, then, to keep in mind that the concepts behind OOP are generally shared among OOP languages, but are not tenets, and are subject to interpretation.

What is the core of OOP? Many books and tutorials mention the three pillars encapsulation, delegation, and polymorphism, but I believe these are traits of a more central concept, which is the **collaboration of entities**. In a well-designed OO system, we can observe a set of actors that send messages to each other to keep the system alive, responsive, and consistent.

These actors have a state, the data, and give access to it through an interface: this is **encapsulation**. Each actor can use functionalities implemented by another sending a message, that is calling a method, and when the relationship between the two is stable we have **delegation**. As communication happens through messages, actors are not concerned with the nature of the recipients, only with their interface, and this is **polymorphism**.

Alan Kay, in his "The Early History of Smalltalk", says

> In computer terms, Smalltalk is a recursion on the notion of computer itself. Instead of dividing "computer stuff" into things each less strong than the whole—like data structures, procedures, and functions which are the usual paraphernalia of programming languages—each Smalltalk object is a recursion on the entire possibilities of the computer. Thus its semantics are a bit like having thousands and thousands of computers all hooked together by a very fast network.

I find this extremely enlightening, as it reveals the idea behind the three pillars, and the reason why we do or don't do certain things in OOP, why we consider good to provide some automatisms or to forbid specific solutions.

By the way, if you replace the word "object" with "microservice" in the quote above, you might be surprised by the description of a very modern architecture for cloud-based systems. Once again, concepts in computer science are like fractals, they are self-similar and pop up in unexpected places.

In this post, I want to focus on the second of the pillars of object-oriented programming: **delegation**. I will discuss its nature and the main two strategies we can follow to implement it: **composition** and **inheritance**. I will provide examples in Python and show how the powerful OOP implementation of this language opens the door to interesting atypical solutions.

For the rest of this post, I will consider objects as mini computers and the system in which they live a "very fast network", using the words of Alan Kay. Data contained in an object is the state of the computer, its methods are the input/output devices, and calling methods is the same thing as sending a message to another computer through the network.

## Delegation in OOP

Delegation is the mechanism through which an actor assigns a task or part of a task to another actor. This is not new in computer science, as any program can be split into blocks and each block generally depends on the previous ones. Furthermore, code can be isolated in libraries and reused in different parts of a program, implementing this "task assignment". In an OO system the assignee is not just the code of a function, but a full-fledged object, another actor.

The main concept to retain here is that the reason behind delegation is **code reuse**. We want to avoid code repetition, as it is often the source of regressions; fixing a bug in one of the repetitions doesn't automatically fix it in all of them, so keeping one single version of each algorithm is paramount to ensure the consistency of a system. Delegation helps us to keep our actors small and specialised, which makes the whole architecture more flexible and easier to maintain (if properly implemented). Changing a very big subsystem to satisfy a new requirement might affect other parts system in bad ways, so the smaller the subsystems the better (up to a certain point, where we incur in the opposite problem, but this shall be discussed in another post).

There is a **dichotomy** in delegation, as it can be implemented following two different strategies, which are orthogonal from many points of view, and I believe that one of the main problems that object-oriented systems have lies in the use of the wrong strategy, in particular the overuse of inheritance. When we create a system using an object-oriented language we need to keep in mind this dichotomy at every step of the design.

There are four areas or points of views that I want to introduce to help you to visualise delegation between actors: **visibility**, **control**, **relationship**, and **entities**. As I said previously, while these concepts apply to systems at every scale, and in particular to every object-oriented language, I will provide examples in Python.

### Visibility: state sharing

The first way to look at delegation is through the lenses of state sharing. As I said before the data contained in an object can be seen as its state, and if hearing this you think about components in a frontend framework or state machines you are on the right path. The state of a computer, its memory or the data on the mass storage, can usually be freely accessed by _internal_ systems, while the access is mediated for _external_ ones. Indeed, the level of access to the state is probably one of the best ways to define internal and external systems in a software or hardware architecture.

When using inheritance, the child class shares its whole state with the parent class. Let's have a look at a simple example

``` python
class Parent:
    def __init__(self, value):
        self._value = value
    
    def describe(self):
        print(f"Parent: value is {self._value}")
    
class Child(Parent):
    pass
    
cld = Child(5)
print(cld._value)
cld.describe()
```

As you can see, `describe` is defined in `Parent`, so when the instance `cld` calls it, its class `Child` delegated the call to the class `Parent`. This, in turn, uses `_value` as if it was defined locally, while it is defined in `cld`. This works because, from the point of view of the state, `Parent` has complete access to the state of `Child`. Please note that the state is not even namespaced, as the state of the child class _becomes_ the state of the parent class.

Composition, on the other side, keeps the state completely private and makes the delegated object see only what is explicitly shared through message passing. A simple example of this is

``` python
class Logger:
    def log(self, value):
        print(f"Logger: value is {value}")


class Process:
    def __init__(self, value):
        self._value = value
        self.logger = Logger()

    def info(self):
        self.logger.log(self._value)

prc = Process(5)

print(prc._value)

prc.info()
```

Here, `Process` objects have an attribute `_value` that is shared with `Logger` objects only when it comes to calling `Logger.log` inside their `info` method. `Logger` objects have no visibility of the state of `Process` objects unless it is explicitly shared.

Note for advanced readers: I'm clearly mixing the concepts of instance and class here, and blatantly ignoring the resulting inconsistencies. The state of an instance is not the same thing as the state of a class, and it should also be mentioned that classes are themselves instances of metaclasses, at least in Python. What I want to point out here is that access to attributes is granted automatically to inherited classes because of the way `__getattribute__` and bound methods work, while in composition such mechanisms are not present and the effect is that the state is not shared.

### Control: implicit and explicit delegation

Another way to look at the dichotomy between inheritance and composition is that of the control we have over the process. Inheritance is usually provided by the language itself and is implemented according to some rules that are part of the definition of the language itself. This makes inheritance an implicit mechanism: when you make a class inherit from another one, there is an automatic and implicit process that rules the delegation between the two, which makes it run outside our control.

Let's see an example of this in action using inheritance

``` python
class Window:
    def __init__(self, title, size_x, size_y):
        self._title = title
        self._size_x = size_x
        self._size_y = size_y

    def resize(self, new_size_x, new_size_y):
        self._size_x = new_size_x
        self._size_y = new_size_y
        self.info()
        
    def info(self):
        print(f"Window '{self._title}' is {self._size_x}x{self._size_y}")


class TransparentWindow(Window):
    def __init__(self, title, size_x, size_y, transparency=50):
        self._title = title
        self._size_x = size_x
        self._size_y = size_y
        self._transparency = transparency

    def change_transparency(self, new_transparency):
        self._transparency = new_transparency
        
    def info(self):
        super().info()
        print(f"Transparency is set to {self._transparency}")       
```

At this point we can instantiate and use `TransparentWindow`

``` python
twin = TransparentWindow("Terminal", 640, 480, 80)
twin.info()
twin.change_transparency(70)
twin.resize(800, 600)
```

When we call `twin.info`, Python is running `TransparentWindow`'s implementation of that method and is not automatically delegating anything to `Window` even though the latter has a method with that name. Indeed, we have to explicitly call it through `super` when we want to reuse it. When we use `resize`, though, the implicit delegation kicks in and we end up with the execution of `Window.resize`. Please note that this delegation doesn't propagate to the next calls, as when `Window.resize` calls `self.info` this runs `TransparentWindow.info`, as the original call was made from that class.

Composition is on the other end of the spectrum, as any delegation performed through composed objects has to be explicit. Let's see an example

``` python
class Body:
    def __init__(self, text):
        self._text = text
    
    def info(self):
        return {
            "length": len(self._text)
        }


class Page:
    def __init__(self, title, text):
        self._title = title
        self._body = Body(text)
        
    def info(self):
        return {
            "title": self._title,
            "body": self._body.info()
        }
```

When we instantiate a `Page` and call `info` everything works

``` python
page = Page("New post", "Some text for an exciting new post")
page.info()
```

but as you can see, `Page.info` has to explicitly mention `Body.info` through `self._body`, as we had to do when using inheritance with `super`. Composition is not different from inheritance when methods are overridden, at least in Python.


### Relationship: to be vs to have

The third point of view from which you can look at delegation is that of the nature of the relationship between actors. Inheritance gives the child class the same nature as the parent class, with specialised behaviour. We can say that a child class implements new features or changes the behaviour of existing ones, but generally speaking, we agree that it _is_ like the parent class. Think about a gaming laptop: it _is_ a laptop, only with specialised features that enable it to perform well in certain situations. On the other end, composition deals with actors that are usually made of other actors of a different nature. A simple example is that of the computer itself, which _has_ a CPU, _has_ a mass storage, _has_ memory. We can't say that the computer _is_ the CPU, because that is reductive.

This difference in the nature of the relationship between actors in a delegation is directly mapped into inheritance and composition. When using inheritance, we implement the verb _to be_

``` python
class Car:
    def __init__(self, colour, max_speed):
        self._colour = colour
        self._speed = 0
        self._max_speed = max_speed
    
    def accelerate(self, speed):
        self._speed = min(speed, self._max_speed)


class SportsCar(Car):
    def accelerate(self, speed):
        self._speed = speed
```

Here, `SportsCar` _is_ a `Car`, it can be initialised in the same way and has the same methods, though it can accelerate much more (wow, that might be a fun ride). Since the relationship between the two actors is best described by _to be_ it is natural to use inheritance.

Composition, on the other hand, implements the verb _to have_ and describes an object that is "physically" made of other objects

``` python
class Employee:
    def __init__(self, name):
        self._name = name


class Company:
    def __init__(self, ceo_name, cto_name):
        self._ceo = Employee(ceo_name)
        self._cto = Employee(cto_name)
```

We can say that a company is the sum of its employees (plus other things), and we easily recognise that the two classes `Employee` and `Company` have a very different nature. They don't have the same interface, and if they have methods with the same name is just by chance and not because they are serving the same purpose.

### Entities: classes or instances

The last point of view that I want to explore is that of the entities involved in the delegation. When we discuss a theoretical delegation, for example saying "This Boeing 747 is a plane, thus it flies" we are describing a delegation between abstract, immaterial objects, namely generic "planes" and generic "flying objects".

``` python
class FlyingObject:
    pass
    
    
class Plane(FlyingObject):
    pass
    
    
boeing747 = Plane()
```

Since `Plane` and `FlyingObject` share the same underlying nature, their relationship is valid for all objects of that type and it is thus established between classes, which are ideas that become concrete when instantiated.

When we use composition, instead, we are putting into play a delegation that is not valid for all objects of that type, but only for those that we connected. For example, we can separate gears from the rest of a bicycle, and it is only when we put together _that_ specific set of gears and _that_ bicycle that the delegation happens. So, while we can think theoretically at bicycles and gears, the actual delegation happens only when dealing with concrete objects.

``` python
class Gears:
    def __init__(self):
        self.current = 1

    def up(self):
        self.current = min(self.current + 1, 8)

    def down(self):
        self.current = max(self.current - 1, 0)


class Bicycle:
    def __init__(self):
        self.gears = Gears()

    def gear_up(self):
        self.gears.up()

    def gear_down(self):
        self.gears.down()

bicycle = Bicycle()
```

As you can see here, an instance of `Bicycle` contains an instance of `Gears` and this allows us to create a delegation in the methods `gear_up` and `gear_down`. The delegation, however, happens between `bicycle` and `bicycle.gears` which are instances.

It is also possible, at least in Python, to have composition using pure classes, which is useful when the class is a pure helper or a simple container of methods (I'm not going to discuss here the benefits or the disadvantages of such a solution)

``` python
class Gears:
    @classmethod
    def up(cls, current):
        return min(current + 1, 8)

    @classmethod
    def down(cls, current):
        return max(current - 1, 0)


class Bicycle:
    def __init__(self):
        self.gears = Gears
        self.current_gear = 1

    def gear_up(self):
        self.current_gear = self.gears.up(self.current_gear)

    def gear_down(self):
        self.current_gear = self.gears.down(self.current_gear)

bicycle = Bicycle()
```

Now, when we run `bicycle.gear_up` the delegation happens between `bicycle`, and instance, and `Gears`, a class. We might extend this forward to have a class which class methods call class methods of another class, but I won't give an example of this because it sounds a bit convoluted and probably not very reasonable to do. But it can be done.

So, we might devise a pattern here and say that in composition there is no rule that states the nature of the entities involved in the delegation, but that most of the time this happens between instances.

Note for advanced readers: in Python, classes are instances of metaclasses, usually `type`, and `type` is an instance of itself, so it is correct to say that composition happens always between instances.

## Bad signs

Now that we looked at the two delegations strategies from different points of view, it's time to discuss what happens when you use the wrong one. You might have heard of the "composition over inheritance" mantra, which comes from the fact that inheritance is often overused. This wasn't and is not helped by the fact that OOP is presented as encapsulation, inheritance, and polymorphism; open a random OOP post or book and you will see this with your own eyes.

Please, bloggers, authors, mentors, teachers, and overall programmers: **stop considering inheritance the only delegation system in OOP**.

That said, I think we should avoid going from one extreme to the opposite, and in general learn to use the tools languages give us. So, let's learn how to recognise the "smell" of bad code!

You are incorrectly using inheritance when:

* There is a clash between attributes with the same name and different meanings. In this case, you are incorrectly sharing the state of a parent class with the child one (visibility). With composition the state of another object is namespaced and it's always clear which attribute you are dealing with.
* You feel the need to remove methods from the child class. This is typically a sign that you are polluting the class interface (relationship) with the content of the parent class. using composition makes it easy to expose only the methods that you want to delegate.

You are incorrectly using composition when:

* You have to map too many methods from the container class to the contained one, to expose them. The two objects might benefit from the automatic delegation mechanism (control) provided by inheritance, with the child class overriding the methods that should behave differently.
* You are composing instances, but creating many class methods so that the container can access them. This means that the nature of the delegation is more related to the code and the object might benefit from inheritance, where the classes delegate the method calls, instead of relying on the relationship between instances.

Overall, code smells for inheritance are the need to override or delete attributes and methods, changes in one class affecting too many other classes in the inheritance tree, big classes that contain heavily unrelated methods. For composition: too many methods that just wrap methods of the contained instances, the need to pass too many arguments to methods, classes that are too empty and that just contain one instance of another class.

## Domain modelling

We all know that there are few cases (in computer science as well as in life) where we can draw a clear line between two options and that most of the time the separation is blurry. There are many grey shades between black and white.

The same applies to composition and inheritance. While the nature of the relationship often can guide us to the best solution, we are not always dealing with the representation of real objects, and even when we do we always have to keep in mind that we are _modelling_ them, not implementing them perfectly.

As a colleague of mine told me once, we have to represent reality with our code, but we have to avoid representing it too faithfully, to avoid bringing reality's limitations into our programs.

I believe this is very true, so I think that when it comes to choosing between composition an inheritance we need to be guided by the nature of the relationship _in our system_. In this, object-oriented programming and database design are very similar. When you design a database you have to think about the domain and the way you extract information, not (only) about the real-world objects that you are modelling.

Let's consider a quick example, bearing in mind that I'm only scratching the surface of something about which people write entire books. Let's pretend we are designing a web application that manages companies and their owners, and we started with the consideration that and `Owner`, well, _owns_ the `Company`. This is a clear composition relationship.

``` python
class Company:
    def __init__(self, name):
        self.name = name

class Owner:
    def __init__(self, first_name, last_name, company_name):
        self.first_name = first_name
        self.last_name = last_name
        self.company = Company(company_name)

owner1 = Owner("John", "Doe", "Pear")
```

Unfortunately, this automatically limits the number of companies owned by an `Owner` to one. If we want to relax that requirement, the best way to do it is to reverse the composition, and make the `Company` contain the `Owner`.

``` python
class Owner:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
class Company:
    def __init__(self, name, owner_first_name, owner_last_name):
        self.name = name
        self.owner = Owner(owner_first_name, owner_last_name)

company1 = Company("Pear", "John", "Doe")
company2 = Company("Pulses", "John", "Doe")
```

As you can see this is in direct contrast with the initial modelling that comes from our perception of the relationship between the two in the real world, which in turn comes from the specific word "owner" that I used. If I used a different word like "president" or "CEO", you would immediately accept the second solution as more natural, as the "president" is one of many employees.

The code above is not satisfactory, though, as it initialises `Owner` every time we create a company, while we might want to use the same instance. Again, this is not mandatory, it depends on the data contained in the `Owner` objects and the level of consistency that we need. For example, if we add to the owner an attribute `online` to mark that they are currently using the website and can be reached on the internal chat, we don't want have to cycle between all companies and set the owner's online status for each of them if the owner is the same. So, we might want to change the way we compose them, passing an instance of `Owner` instead of the data used to initialise it.

``` python
class Owner:
    def __init__(self, first_name, last_name, online=False):
        self.first_name = first_name
        self.last_name = last_name
        self.online = online
        
class Company:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        
owner1 = Owner("John", "Doe")
company1 = Company("Pear", owner1)
company2 = Company("Pulses", owner1)
```

Clearly, if the class `Company` has no other purpose than having a name, using a class is overkill, so this design might be further reduced to an `Owner` with a list of company names.

``` python
class Owner:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.companies = []
        
owner1 = Owner("John", "Doe")
owner1.companies.extend(["Pear", "Pulses"])
```

Can we use inheritance? Now I am stretching the example to its limit, but I can accept there might be a use case for something like this.

``` python
class Owner:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
class Company(Owner):
    def __init__(self, name, owner_first_name, owner_last_name):
        self.name = name
        super().__init__(owner_first_name, owner_last_name)

company1 = Company("Pear", "John", "Doe")
company2 = Company("Pulses", "John", "Doe")
```

As I showed in the previous sections, though, this code smells as soon as we start adding something like the `email` address.

``` python
class Owner:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        
class Company(Owner):
    def __init__(self, name, owner_first_name, owner_last_name, email):
        self.name = name
        super().__init__(owner_first_name, owner_last_name, email)

company1 = Company("Pear", "John", "Doe")
company2 = Company("Pulses", "John", "Doe")
```

Is `email` that of the company or the personal one of its owner? There is a clash, and this is a good example of "state pollution": both attributes have the same name, but they represent different things and might need to coexist.

In conclusion, as you can see we have to be very careful to discuss relationships between objects in the context of our domain and avoid losing connection with the business logic.

## Mixing the two: composed inheritance

Speaking of blurry separations, Python offers an interesting hook to its internal attribute resolution mechanism which allows us to create a hybrid between composition and inheritance that I call "composed inheritance".

Let's have a look at what happens internally when we deal with classes that are linked through inheritance.

```
class Parent:
    def __init__(self, value):
        self.value = value
        
    def info(self):
        print(f"Value: {self.value}")

class Child(Parent):
    def is_even(self):
        return self.value % 2 == 0

c = Child(5)
c.info()
c.is_even()
```

This is a trivial example of an inheritance relationship between `Child` and `Parent`, where `Parent` provides the methods `__init__` and `info` and `Child` augments the interface with the method `is_even`.

Let's have a look at the internals of the two classes. `Parent.__dict__` is

``` python
mappingproxy({'__module__': '__main__',
              '__init__': <function __main__.Parent.__init__(self, value)>,
              'info': <function __main__.Parent.info(self)>,
              '__dict__': <attribute '__dict__' of 'Parent' objects>,
              '__weakref__': <attribute '__weakref__' of 'Parent' objects>,
              '__doc__': None}
```

and `Child.__dict__` is

``` python
mappingproxy({'__module__': '__main__',
              'is_even': <function __main__.Child.is_even(self)>,
              '__doc__': None})
```

Finally, the bond between the two is established through `Child.__bases__`, which has the value `(__main__.Parent,)`.

So, when we call `c.is_even` the instance has a bound method that comes from the class `Child`, as its `__dict__` contains the function `is_even`. Conversely, when we call `c.info` Python has to fetch it from `Parent`, as `Child` can't provide it. This mechanism is implemented by the method `__getattribute__` that is the core of the Python inheritance system.

As I mentioned before, however, there is a hook into this system that the language provides us, namely the method `__getattr__`, which is not present by default. What happens is that when a class can't provide an attribute, Python _first_ tries to get the attribute with the standard inheritance mechanism but if it can't be found, as a last resort it tries to run `__getattr__` passing the attribute name.

An example can definitely clarify the matter.

``` python
class Parent:
    def __init__(self, value):
        self.value = value
        
    def info(self):
        print(f"Value: {self.value}")

class Child(Parent):
    def is_even(self):
        return self.value % 2 == 0
        
    def __getattr__(self, attr):
        if attr == "secret":
            return "a_secret_string"
        
        raise AttributeError

c = Child(5)
```

Now, if we try to access `c.secret`, Python would raise an `AttributeError`, as neither `Child` nor `Parent` can provide that attribute. As a last resort, though, Python runs `c.__getattr__("secret")`, and the code of that method that we implemented in the class `Child` returns the string `"a_secret_string"`. Please note that the value of the argument `attr` is the _name_ of the attribute as a string.

Because of the catch-all nature of `__getattr__`, we eventually have to raise an `AttributeError` to keep the inheritance mechanism working, unless we actually need or want to implement something very special.

This opens the door to an interesting hybrid solution where we can compose objects retaining an automatic delegation mechanism.

``` python
class Parent:
    def __init__(self, value):
        self.value = value
        
    def info(self):
        print(f"Value: {self.value}")

class Child:
    def __init__(self, value):
        self.parent = Parent(value)
    
    def is_even(self):
        return self.value % 2 == 0
        
    def __getattr__(self, attr):
        return getattr(self.parent, attr)
        
c = Child(5)
c.value
c.info()
c.is_even()
```

As you can see, here `Child` is composing `Parent` and there is no inheritance between the two. We can nevertheless access `c.value` and call `c.info`, thanks to the face that `Child.__getattr__` is delegating everything can't be found in `Child` to the instance of `Parent` stored in `self.parent`.

Note: don't confuse `getattr` with `__getattr__`. The former is a builtin function that gets an attribute provided its name, a replacement for the dotted notation when the name of the attribute is known as a string. The latter is the hook into the inheritance mechanism that I described in this section.

Now, this is very powerful, but is it also useful?

I think this is not one of the techniques that will drastically change the way you write code in Python, but it can definitely help you to use composition instead of inheritance even when the amount of methods that you have to wrap is high. One of the limits of composition is that you are at the extreme spectrum of automatism; while inheritance is completely automatic, composition doesn't do anything for you. This means that when you compose objects you need to decide which methods or attributes of the contained objects you want to wrap, in order to expose then in the container object. In the previous example, the class `Child` might want to expose the attribute `value` and the method `info`, which would result in something like

``` python
class Parent:
    def __init__(self, value):
        self.value = value
        
    def info(self):
        print(f"Value: {self.value}")

class Child:
    def __init__(self, value):
        self.parent = Parent(value)
    
    def is_even(self):
        return self.value % 2 == 0
    
    def info(self):
        return self.parent.info()
    
    @property
    def value(self):
        return self.parent.value
```

As you can easily see, the more `Child` wants to expose of the `Parent` interface, the more wrapper methods and properties you need. To be perfectly clear, in this example the code above smells, as there are too many one-liner wrappers, which tells me it would be better to use inheritance. But if the class `Child` had a dozen of its own methods, suddenly it would make sense to do something like this, and in that case, `__getattr__` might come in handy.

## Final words

Both composition and inheritance are tools, and both exist to serve the bigger purpose of code reuse, so learn their strength and their weaknesses, so that you might be able to use the correct one and avoid future issues in your code.

I hope this rather long discussion helped you to get a better picture of the options you have when you design an object-oriented system, and also maybe introduced some new ideas or points of view if you are already comfortable with the concepts I wrote about.

## Feedback

Feel free to reach me on [Twitter](https://twitter.com/thedigicat) if you have questions. The [GitHub issues](https://github.com/TheDigitalCatOnline/thedigitalcatonline.github.com/issues) page is the best place to submit corrections.

