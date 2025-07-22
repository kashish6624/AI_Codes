import random

# Function to take input from the user for the input-output table
def get_input_output_table():
    while True:
        try:
            rows = int(input("Enter the number of rows in the input-output table: "))
            if rows <= 0:
                print("Number of rows must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    table = []
    print("Enter the values of a, b, c, and z (separated by spaces):")
    for _ in range(rows):
        while True:
            try:
                row = list(map(int, input().split()))
                if len(row) != 4:
                    print("Please enter exactly 4 integers (a, b, c, z).")
                    continue
                table.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter 4 integers separated by spaces.")
    return table

# Function to calculate output Z'
def calculate_output(chromosome, a, b, c):
    Y = chromosome[0] * a + chromosome[1] * b + chromosome[2] * c
    return 1 if Y >= 0 else 0

# Fitness function: number of correct entries
def fitness_function(chromosome, data):
    return sum(1 for a, b, c, z in data if calculate_output(chromosome, a, b, c) == z)

# Create initial population
def create_population(population_size, weight_values):
    return [[random.choice(weight_values) for _ in range(3)] for _ in range(population_size)]

# Selection: choose two parents based on fitness
def selection(population, data):
    return sorted(population, key=lambda x: fitness_function(x, data), reverse=True)[:2]

# Crossover: combine two parents to produce offspring
def crossover(parent1, parent2):
    crossover_point = random.randint(1, 2)
    return parent1[:crossover_point] + parent2[crossover_point:]

# Mutation: randomly change one weight in a chromosome
def mutation(chromosome, mutation_rate, weight_values):
    if random.random() < mutation_rate:
        mutation_index = random.randint(0, 2)
        new_value = random.choice(weight_values)
        while new_value == chromosome[mutation_index]:  # Ensure mutation changes the value
            new_value = random.choice(weight_values)
        chromosome[mutation_index] = new_value
    return chromosome

# GA Main loop
def genetic_algorithm(data, population_size, generations, mutation_rate):
    weight_values = [-1, 0, 1]  # Possible weight values
    population = create_population(population_size, weight_values)

    for generation in range(generations):
        new_population = []
        for _ in range(population_size):
            # Selection
            parents = selection(population, data)
            # Crossover
            offspring = crossover(parents[0], parents[1])
            # Mutation
            offspring = mutation(offspring, mutation_rate, weight_values)
            new_population.append(offspring)

        population = new_population

        # Check if a solution is found
        for chromosome in population:
            if fitness_function(chromosome, data) == len(data):  # Fitness == number of rows
                print(f"Solution found in generation {generation}: {chromosome}")
                return chromosome

    print("No exact solution found after all generations.")
    return None

# Main function to get user input and run the GA
def main():
    # Get input-output table from the user
    data = get_input_output_table()

    # Get other parameters from the user
    while True:
        try:
            population_size = int(input("Enter the population size: "))
            generations = int(input("Enter the number of generations: "))
            mutation_rate = float(input("Enter the mutation rate (0 to 1): "))
            if population_size <= 0 or generations <= 0 or not (0 <= mutation_rate <= 1):
                print("Population size and generations must be positive, and mutation rate must be between 0 and 1.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    # Run the genetic algorithm to find the solution
    solution = genetic_algorithm(data, population_size, generations, mutation_rate)

    # Output the solution
    if solution:
        print(f"The solution is: {solution}")
    else:
        print("No solution found. Consider adjusting parameters or increasing generations.")

# Run the main function
if __name__ == "__main__":
    main()




"""import random
import numpy as np

def get_user_input():
    num_jobs = int(input("Enter the number of jobs: "))
    num_machines = int(input("Enter the number of machines: "))

    jobs_data = []
    for i in range(num_jobs):
        print(f"\nEnter the machine and processing time for Job {i + 1}:")
        job = []
        for j in range(num_machines):
            machine_id = int(input(f"  Machine {j + 1} ID: "))
            processing_time = int(input(f"  Processing time on Machine {machine_id}: "))
            job.append((machine_id, processing_time))
        jobs_data.append(job)
    
    return jobs_data, num_jobs, num_machines

population_size = 20
num_generations = 100
mutation_rate = 0.1
tournament_size = 5
elitism = True

def generate_initial_population(jobs_data, num_jobs):
    population = []
    for _ in range(population_size):
        individual = []
        for job_id in range(num_jobs):
            individual.extend([job_id] * len(jobs_data[job_id]))  # Ensure each job ID appears correct number of times
        random.shuffle(individual)
        population.append(individual)
    return population

def decode_schedule(chromosome, jobs_data, num_jobs, num_machines):
    job_counters = [0] * num_jobs  # Tracks the operation number for each job
    machine_time = [0] * num_machines  # Tracks the current time on each machine
    job_end_time = [0] * num_jobs  # Tracks the end time for each job

    for gene in chromosome:
        job_id = gene
        operation_index = job_counters[job_id]
        if operation_index >= len(jobs_data[job_id]):
            print(f"Error: operation_index {operation_index} out of range for job {job_id}.")
            return float('inf')  # Return a large number indicating invalid solution
        
        machine_id, processing_time = jobs_data[job_id][operation_index]
        start_time = max(machine_time[machine_id], job_end_time[job_id])
        end_time = start_time + processing_time
        machine_time[machine_id] = end_time
        job_end_time[job_id] = end_time
        job_counters[job_id] += 1  # Move to the next operation for this job

    makespan = max(job_end_time)  # The makespan is the maximum completion time across all jobs
    return makespan

def fitness(chromosome, jobs_data, num_jobs, num_machines):
    makespan = decode_schedule(chromosome, jobs_data, num_jobs, num_machines)
    return 1.0 / makespan if makespan > 0 else float('inf')

def tournament_selection(population, jobs_data, num_jobs, num_machines):
    tournament = random.sample(population, tournament_size)
    fittest = max(tournament, key=lambda x: fitness(x, jobs_data, num_jobs, num_machines))
    return fittest

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(chromosome)), 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

def genetic_algorithm(jobs_data, num_jobs, num_machines):
    population = generate_initial_population(jobs_data, num_jobs)
    
    for generation in range(num_generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = tournament_selection(population, jobs_data, num_jobs, num_machines)
            parent2 = tournament_selection(population, jobs_data, num_jobs, num_machines)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        
        if elitism:
            best_individual = max(population, key=lambda x: fitness(x, jobs_data, num_jobs, num_machines))
            new_population[random.randint(0, population_size - 1)] = best_individual
        
        population = new_population
        best_fitness = max(population, key=lambda x: fitness(x, jobs_data, num_jobs, num_machines))
        print(f"Generation {generation + 1}, Best Makespan: {1.0 / fitness(best_fitness, jobs_data, num_jobs, num_machines)}")
    
    best_solution = max(population, key=lambda x: fitness(x, jobs_data, num_jobs, num_machines))
    return best_solution, 1.0 / fitness(best_solution, jobs_data, num_jobs, num_machines)

if __name__ == "__main__":
    jobs_data, num_jobs, num_machines = get_user_input()
    best_chromosome, best_makespan = genetic_algorithm(jobs_data, num_jobs, num_machines)
    
    print("\nBest Schedule (Chromosome):", best_chromosome)
    print("Best Makespan:", best_makespan)
"""