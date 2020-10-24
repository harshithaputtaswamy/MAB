import random
from tqdm import tqdm
import math


class agent():
    def __init__(self):
        self.n = 10
        self.m = 5
        self.count = [0]*self.n
        self.mean_r = [0]*self.n
        self.total_count = 0
        self.reward = [0]*self.n
        self.actual_mean = [random.uniform(0, 1) for i in range(self.n)]

    # def file_name():

    def select_hashtags(self):
        selcted_hashtags = []
        ucb_values = []
        for i in range(self.n):
            if self.count[i] > 0:
                exploration = math.sqrt(
                    (2 * math.log(self.total_count)) / (self.count[i]))
            else:
                exploration = 1e400
            update_value = self.mean_r[i] + exploration
            # ucb_values.append(update_value)
            ucb_values.append((i, update_value))
        ucb_values = sorted(ucb_values, key=lambda x: x[1], reverse=True)
        for i in range(self.m):
            selcted_hashtags.append(ucb_values[0][0])
            del (ucb_values[0])
        # for i in range(self.m):
        #     selcted_hashtags.append(ucb_values.index(max(ucb_values)))
        #     ucb_values.remove(max(ucb_values))
        self.total_count += 1
        return selcted_hashtags

    def update_mean(self, reward):
        selected_hashtags = self.select_hashtags()
        for i in selected_hashtags:
            self.mean_r[i] = (
                self.mean_r[i]*self.count[i] + reward[i])/(self.count[i] + 1)
            self.count[i] += 1
        print(selected_hashtags)
        return 1

    def reward_gen(self):
        for i in range(self.n):
            if(random.random() < self.actual_mean[i]):
                self.reward[i] = 1
            else:
                self.reward[i] = 0
        return self.reward


cur_agent = agent()
for i in tqdm(range(200000)):
    reward = cur_agent.reward_gen()
    check = cur_agent.update_mean(reward)
print('mean_reward', cur_agent.mean_r)
