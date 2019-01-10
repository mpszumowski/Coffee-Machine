# Coffee-Machine
Coffee machine simulation, an exercise in OOP and design patterns

### 1. Factory design pattern

Coffee machine-factory knows how to apply production steps for each product.
Coffee programs-products are defined independently in `./coffees` directory.
Each is based on abstract product interface and implements
(1) ingredients and (2) procedure to follow. As a consequence:<br>
1. It is easy to modify or create new programs.
Coffee Machine loads them dynamically from `./coffees` dir.
2. Procedure can be extended to use additional information,
like brewing temperature, new ingredients.

### 2. Configuration decouplement

`config.json` holds information that is configurable by user.
`params.json` holds parameters specific to given model of the machine.

### 3. Machine and components decouplement

Coffee machine must expose methods to prepare given
type of coffee, check if its ready and notify user
about necessary actions.
1. Coffee preparation steps are dispatched based on
ingredient type in order provided by product (coffee program).
2. Machine is ready if all of its components are ready.
3. Each component monitors its own state, so that
any refactoring of component logic does not entail
any changes in main machine code.

#### 4. Observer design pattern

The components are attached to the machine and use notify method
to pass information about their state. This may seem as
an overkill since observer pattern is designed for many-to-one
relationships, whereas one component should have only one machine
it is attached to. Other than that, general observer logic
applies and thus:
1. There is sufficient level of indirection so that the machine
does not need to manually control the state of each of its components.

