def load_functions():
    functions = {"Admin Programs": [],
                 "Super Admin Programs": [],
                 "Basic Programs": [],
                 "API Programs": [],
                 "Healthcare Programs": []
    }

    # Admin Functions
    functions['Admin Programs'].append(['Code'
                                        ]
                                    )

    # Super Admin Functions
    functions['Super Admin Programs'].append(['Show Data',
                                              ]
                                            )

    # Basic Functions
    functions['Basic Programs'].append(['Advice Quotes', 
                                        'My IP Address', 
                                        'Jokes', 
                                        'My Location'
                                        ]
                                    )

    # API Functions
    functions['API Programs'].append(['Calculator', 
                                      'Temperature Condition', 
                                      'Weather Condition', 
                                      'Latest News', 
                                      'Space News', 
                                      'Mars Images', 
                                      'Astroids', 
                                      'Solar Bodies', 
                                      'Movies', 
                                      'TV Shows', 
                                      'About Actors',
                                      ]
                                    )

    #Healthcare Functions
    functions['Healthcare Programs'].append(['Diabetes Test'
                                              ]
                                            )

    # Return all the functions
    return functions

# print(load_functions())
