## Java Functional Interfaces: `Function`, `Supplier`, `Consumer`, and `Runnable`

This document explains four important functional interfaces in Java:

- **`Function<T, R>`**
- **`Supplier<T>`**
- **`Consumer<T>`**
- **`Runnable`**

These are used heavily with **lambdas** and **method references**, and they let you pass behavior (code) as data.

---

## Cheat Sheet (Quick Reference)

- **Function\<T, R\>**
  - **Shape**: takes `T`, returns `R` → `R apply(T t)`
  - **Use**: transformations (`map`, conversions, scoring functions).
- **Supplier\<T\>**
  - **Shape**: takes nothing, returns `T` → `T get()`
  - **Use**: lazy values, defaults, expensive object creation on demand.
- **Consumer\<T\>**
  - **Shape**: takes `T`, returns nothing → `void accept(T t)`
  - **Use**: side effects on a value (logging, saving, sending).
- **Runnable**
  - **Shape**: takes nothing, returns nothing → `void run()`
  - **Use**: a unit of work, often for threads or schedulers.
- **Functional interface**
  - **Meaning**: exactly one abstract method (e.g., `run`, `apply`, `get`, `accept`).
  - **Why**: is the target type for lambdas and method references.
- **Lambda**
  - **Idea**: concise implementation of a functional interface, e.g. `x -> x * 2;`.
  - **Why**: removes anonymous-class boilerplate, powers Streams and callbacks.
- **Anonymous class**
  - **Idea**: inline class without a name, e.g. `new Runnable() { public void run() { ... } }`.
  - **Use**: when you need a one-off implementation with multiple methods or extra state.
- **Interface vs class**
  - **Interface**: contract/capability (no instances, no per-object state, can have abstract/default/static methods).
  - **Class**: blueprint for concrete objects with fields, constructors, and full implementations.

---

## Big Picture

Each interface answers two questions:

1. **Does it take input?**
2. **Does it return a value?**

Summary:

- **`Function<T, R>`**: takes **one input**, returns **one output**.
- **`Supplier<T>`**: takes **no input**, returns **a value**.
- **`Consumer<T>`**: takes **one input**, returns **nothing** (side effects only).
- **`Runnable`**: takes **no input**, returns **nothing** (just "do this action").

This distinction is why they’re useful: you can describe *what shape of behavior* you expect, and then pass in whatever implementation you want.

---

## `Function<T, R>`

**What it is**: A function that takes one input and returns one output.

- **Method**: `R apply(T t)`
- **Signature**: `Function<InputType, ResultType>`

**Example:**

```java
import java.util.function.Function;

Function<String, Integer> lengthFn = s -> s.length();
int len = lengthFn.apply("Hello"); // 5
```

**Why it’s useful:**

- Encapsulates “convert X to Y” logic (e.g., `String` → `Integer`, `Shoe` → `Double` score).
- Widely used in the Streams API (`map`, etc.).

**Streams example:**

```java
import java.util.List;

List<String> names = List.of("Alice", "Bob");
List<Integer> lengths = names.stream()
                             .map(s -> s.length())  // Function<String, Integer>
                             .toList();
```

---

## `Supplier<T>`

**What it is**: A function that takes no input and returns a value.

- **Method**: `T get()`
- **Signature**: `Supplier<ResultType>`

**Example:**

```java
import java.util.function.Supplier;

Supplier<Double> randomSupplier = () -> Math.random();
double r = randomSupplier.get();
```

**Why it’s useful:**

- **Lazy creation**: “Give me a value *when* I ask, not now.”
- Good for:
  - Delayed computation
  - Expensive object creation
  - Default values (e.g., `Map.computeIfAbsent`)

---

## `Consumer<T>`

**What it is**: A function that takes one input and returns nothing.

- **Method**: `void accept(T t)`
- **Signature**: `Consumer<InputType>`

**Example:**

```java
import java.util.function.Consumer;

Consumer<String> printer = s -> System.out.println("Value: " + s);
printer.accept("Hello");
```

**Why it’s useful:**

- Represents “do something with this value”:
  - Logging
  - Saving to a database
  - Sending over a network
- Common in Streams (`forEach`) and event/callback APIs.

---

## `Runnable`

**What it is**: A function that takes no input and returns nothing.

- **Method**: `void run()`
- **Signature**: `Runnable` (no generics)

**Example:**

```java
Runnable task = () -> System.out.println("Running in a thread");
new Thread(task).start();
```

**Why it’s useful:**

- Represents a **unit of work** to be executed later.
- Used for:
  - `Thread`
  - Executor services
  - Timers
  - UI callbacks

---

## How They Relate

Viewed together:

- **`Function<T, R>`**: input and output.
- **`Supplier<R>`**: output only.
- **`Consumer<T>`**: input only.
- **`Runnable`**: neither input nor output (just side effects).

This set covers the most common shapes of behavior you need to pass around.

---

## Realistic Example with a `ShoeService`

Below is a small example that uses **all four** interfaces in a plausible domain: a shoe inventory/service.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.function.Supplier;
import java.util.function.Consumer;

class Shoe {
    String name;
    double price;
    double comfortScore; // 1–10

    Shoe(String name, double price, double comfortScore) {
        this.name = name;
        this.price = price;
        this.comfortScore = comfortScore;
    }
}

class ShoeService {

    // 1) Function: transform a Shoe into something else (e.g., its "score")
    public double scoreShoe(Shoe shoe, Function<Shoe, Double> scoringFunction) {
        return scoringFunction.apply(shoe);
    }

    // 2) Supplier: lazily provide default shoes (e.g., when DB is empty)
    public List<Shoe> loadShoes(Supplier<List<Shoe>> shoeSupplier) {
        // In a real app, you might check cache/DB first, then fall back:
        return shoeSupplier.get();
    }

    // 3) Consumer: "do something" with each shoe (log it, save it, send it, etc.)
    public void processShoes(List<Shoe> shoes, Consumer<Shoe> action) {
        for (Shoe shoe : shoes) {
            action.accept(shoe);
        }
    }

    // 4) Runnable: run a unit of work (e.g., background maintenance job)
    public void runMaintenanceTask(Runnable task) {
        // Could be: new Thread(task).start(); or submit to an executor
        task.run();
    }
}

public class Main {
    public static void main(String[] args) {
        ShoeService service = new ShoeService();

        List<Shoe> inventory = new ArrayList<>();
        inventory.add(new Shoe("Runner 1", 120.0, 8.5));
        inventory.add(new Shoe("Casual 2", 80.0, 7.0));

        // Function: "How good is this shoe?" (simple formula)
        Function<Shoe, Double> valueScore = shoe ->
                shoe.comfortScore * 10 - shoe.price * 0.2;

        double score = service.scoreShoe(inventory.get(0), valueScore);
        System.out.println("Score of first shoe: " + score);

        // Supplier: provide a default inventory if needed
        Supplier<List<Shoe>> defaultInventorySupplier = () -> {
            List<Shoe> defaults = new ArrayList<>();
            defaults.add(new Shoe("Default Runner", 100.0, 8.0));
            return defaults;
        };

        List<Shoe> loadedShoes = service.loadShoes(defaultInventorySupplier);
        System.out.println("Loaded " + loadedShoes.size() + " default shoe(s)");

        // Consumer: print each shoe nicely
        Consumer<Shoe> printer = shoe ->
                System.out.println("Shoe: " + shoe.name +
                        ", price=" + shoe.price +
                        ", comfort=" + shoe.comfortScore);

        service.processShoes(inventory, printer);

        // Runnable: background clean‑up task
        Runnable maintenance = () ->
                System.out.println("Running nightly maintenance: reindexing shoes...");

        service.runMaintenanceTask(maintenance);
    }
}
```

### What Each Interface Does Here

- **`Function<Shoe, Double>`** (`valueScore`):
  - Defines *how to calculate a numeric score* from a `Shoe`.
- **`Supplier<List<Shoe>>`** (`defaultInventorySupplier`):
  - Defines *how to produce a default list of shoes* when needed.
- **`Consumer<Shoe>`** (`printer`):
  - Defines *what to do with each shoe* (print, but could be save/log/etc.).
- **`Runnable`** (`maintenance`):
  - Defines *a unit of work* (maintenance task) with no input or output.

Together, these interfaces let the `ShoeService` be flexible: the service decides **when** to use the behavior, and the caller decides **what** that behavior is.

---

## Functional Interfaces (Concept)

Beyond specific types like `Function` and `Supplier`, Java has the broader idea of a **functional interface**.

- **Definition**: An interface with **exactly one abstract method**.
- **Examples**:
  - `Runnable` → `void run();`
  - `Function<T, R>` → `R apply(T t);`
  - `Supplier<T>` → `T get();`
  - `Consumer<T>` → `void accept(T t);`
- **Why they matter**:
  - They are the **target types** for lambdas and method references.
  - They express “a piece of behavior of this shape” (e.g., “takes a `T`, returns an `R`”).
  - Many modern APIs (Streams, `CompletableFuture`, etc.) are built around them.

You can mark your own functional interface with `@FunctionalInterface`:

```java
@FunctionalInterface
interface StringTransformer {
    String transform(String s);
}
```

This annotation is optional but recommended; it tells the compiler to enforce that there is only **one** abstract method.

---

## Lambdas in Java

A **lambda expression** is a concise way to provide an implementation of a functional interface.

General shapes:

- **Single expression**:

```java
x -> x * 2;
```

- **Block with multiple statements**:

```java
(x, y) -> {
    int sum = x + y;
    return sum;
};
```

You can use a lambda **anywhere** a functional interface is expected.

### Examples

- **`Runnable`**:

```java
Runnable r = () -> System.out.println("Running");
```

- **`Consumer<String>`**:

```java
Consumer<String> printer = s -> System.out.println("Hello " + s);
```

- **`Function<String, Integer>`**:

```java
Function<String, Integer> lengthFn = s -> s.length();
```

- **Streams**:

```java
List<String> names = List.of("Alice", "Bob");

List<Integer> lengths = names.stream()
                             .map(s -> s.length())  // lambda
                             .toList();
```

### Why lambdas are useful

- **Less boilerplate** than anonymous inner classes.
- Make it easy to pass “what to do” into methods (sorting rules, event handlers, transformation logic).
- Power the **Streams API** and functional programming style in Java.
- Encourage designing APIs around **behavior** rather than just data.

---

## Anonymous Classes

An **anonymous class** is a class without a name, defined and instantiated inline, usually as a one-off implementation of an interface or a class.

### Example (pre-lambda style)

```java
Runnable r = new Runnable() {
    @Override
    public void run() {
        System.out.println("Running");
    }
};
```

### When anonymous classes are useful

- One-off implementations of:
  - Interfaces (listeners, callbacks)
  - Abstract classes
  - Concrete classes when you want to override a method for a specific use
- When you need:
  - Multiple methods overridden
  - Extra fields or state on this specific instance
  - To extend a **class**, not just implement an interface (lambdas can’t extend classes).

### Anonymous classes vs lambdas

For functional interfaces, this anonymous style:

```java
Runnable r = new Runnable() {
    @Override
    public void void run() {
        System.out.println("Running");
    }
};
```

is equivalent in behavior to this lambda:

```java
Runnable r = () -> System.out.println("Running");
```

Lambdas are usually preferred for functional interfaces because they are **shorter**, **clearer**, and emphasize that you are just passing a **piece of behavior** rather than defining a full-blown class.

---

## Interfaces vs Classes in Java

Understanding the difference between **interfaces** and **classes** is important background for functional interfaces and lambdas.

### High-level idea

- **Class**: A *blueprint for objects* that can have **state** (fields) and **full behavior** (methods, constructors). You create **instances** of classes.
- **Interface**: A *contract* that says “any class that implements me must provide these methods.” It describes **capabilities** or an API.

### Key differences

- **Instantiation**
  - **Class**: Can usually be instantiated (if not `abstract`): `Dog d = new Dog();`
  - **Interface**: Cannot be instantiated directly.
- **State (fields)**
  - **Class**: Can have instance fields that vary per object.
  - **Interface**: Fields are implicitly `public static final` (constants only), no per-instance state.
- **Methods**
  - **Class**:
    - Can have instance methods, static methods, and constructors.
    - Methods are fully implemented.
  - **Interface**:
    - Traditionally only abstract methods.
    - Since Java 8, may also have `default` and `static` methods with implementations.
    - No constructors.
- **Inheritance / implementation**
  - **Class**:
    - Can extend **one** other class.
    - Can implement **multiple** interfaces.
  - **Interface**:
    - Can extend **multiple** interfaces.
    - Is implemented by classes (or extended by other interfaces).
- **Typical use**
  - **Class**: Concrete things with data + behavior (`Shoe`, `Order`, `Dog`).
  - **Interface**: Roles/capabilities/APIs that multiple classes can implement (`List`, `Map`, `Comparable`, `Runnable`, `Function`).

### Intuition

- Use an **interface** to say: “Anything that **implements this** can be used **here**.”
- Use a **class** to say: “This is a specific kind of object with actual data and behavior.”
