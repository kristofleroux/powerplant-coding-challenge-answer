# Powerplant Coding Challenge

###Installation

We have included a Dockerfile for easy usage.

It will use the latest stable Debian Release (Buster), install Python 3.8, all needed python packages and
the coincbc-or solver executable.

Then it will run the flask REST API and flask-socketio server for you to use.

####Steps

- Make sure you have installed docker, change to the root directory of this project and type in the command line:

    `docker build -t ppcc:latest .`

- After building, run the docker image as a container, autoremove when stopped, interactive and expose port 5000 with:

    `docker run -it --rm -p 5000:5000 ppcc:latest`

###Usage

As soon as the container is done initializing, browse with a webbrowser to:

    http://localhost:5000/

Send a POST request to:

    http://0.0.0.0:5000/calc

with the header:

    Content-Type: application/json

and the body (your payload) eg.:

    {
    "load": 780,
    "fuels":
        {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        },
    "powerplants": [
        {
            "name": "gasfiredbig1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "gasfiredbig2",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "gasfiredsomewhatsmaller",
            "type": "gasfired",
            "efficiency": 0.37,
            "pmin": 40,
            "pmax": 210
        },
        {
            "name": "tj1",
            "type": "turbojet",
            "efficiency": 0.3,
            "pmin": 0,
            "pmax": 16
        },
        {
            "name": "windpark1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
        },
        {
            "name": "windpark2",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 36
        }
    ]
}

The resonse for this example will be:

    [
      {
        "name": "gasfiredbig1",
        "p": 0
      },
      {
        "name": "gasfiredbig2",
        "p": 384
      },
      {
        "name": "gasfiredsomewhatsmaller",
        "p": 210
      },
      {
        "name": "tj1",
        "p": 0
      },
      {
        "name": "windpark1",
        "p": 150
      },
      {
        "name": "windpark2",
        "p": 36
      }
    ]

 If you check your browser again, the response should also be displayed on the page, using sockets.

###Functionalities

- REST-API
- Websockets
- Docker
- CO2 Addition

- TODO: Add error handling.
- TODO: Check if solver has a feasible solution, otherwise clean error handling, now server error 500.

    ```python
    # TODO: check if m is feasible

    # if (m.solver.status == SolverStatus.ok) and (
    #         m.solver.termination_condition == TerminationCondition.optimal):
    #     pass
    # elif (m.solver.termination_condition == TerminationCondition.infeasible):
    #     pass
    # else:
    #     # Something else is wrong
    #     print("SolverStatus: " + m.solver.status)
    ```

- TODO: Create an extra template for a visualization of the solution using matplotlib and plotly.

    ```python
    # TODO: make extra template and use matplotlib and plotly to output a graph with the solution
    #
    # fig, ax = plt.subplots(max(m.N) + 1, 1, figsize=(8, 1.5 * max(m.N) + 1))
    # for n in range(1, max(m.N)+1):
    #     ax[n].bar(1, m.x[n]())
    #     ax[n].set_xlim(0, 2)
    #     ax[n].set_ylim(0, 1.1 * pmaxs[n-1])
    #     ax[n].plot(ax[n].get_xlim(), np.array([pmaxs[n-1], pmaxs[n-1]]), 'r--')
    #     ax[n].plot(ax[n].get_xlim(), np.array([pmins[n-1], pmins[n-1]]), 'r--')
    #     ax[n].set_title('Unit ' + str(n))
    # fig.tight_layout()
    #
    # plt.show()
    ```

- TODO: use aiohttp and asyncio for async REST handling and async workers.
- TODO: pytest unit tests
- TODO: better optim model in pyomo, mixed integer programming
- TODO: Look at other optim libraries like mosek






Prerequisites:
- Python 3 or higher
- pip install -r requirements.txt
- pyomo needs coinor-cbc solver
