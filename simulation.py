from random import random


class MarkovChain:
    def __init__(self, state_list, probability_dict, initial_state=None) -> None:
        self.state_list = state_list
        self.probability_dict = probability_dict
        self.current_state = self.init_system(initial_state)
        print(f"初始化完成，当前状态: {self.current_state}")

    def init_system(self, initial_state):
        """初始化系统，设置初始状态"""
        self.calibrate_probability_dict()  # 先校准概率字典
        self.validate_probability_dict()  # 再验证概率字典
        if initial_state is None:
            if not self.state_list:
                raise ValueError("状态列表 state_list 不能为空")
            return self.state_list[0]
        if initial_state not in self.state_list:
            raise ValueError(f"初始状态 {initial_state} 不在状态列表中")
        return initial_state

    def calibrate_probability_dict(self) -> None:
        """自动校准概率字典，确保每个状态的概率总和为1"""
        for state in self.state_list:
            if state not in self.probability_dict:
                continue
            total_prob = sum(self.probability_dict[state].values())
            for next_state in self.state_list:
                if next_state in self.probability_dict[state]:
                    self.probability_dict[state][next_state] /= total_prob

    def validate_probability_dict(self):
        """验证概率字典和状态列表的正确性"""
        for state in self.state_list:
            if state not in self.probability_dict:
                continue
            if not abs(sum(self.probability_dict[state].values()) - 1) < 1e-6:  # 允许小的浮点数误差
                raise ValueError(f"状态 {state} 的概率总和不为1: {sum(self.probability_dict[state].values())}")
            for next_state in self.state_list:
                if next_state not in self.probability_dict[state]:
                    raise ValueError(f"状态 {state} 到状态 {next_state} 的概率不存在")

    def transfer_state(self):
        """根据当前状态，转移到下一个状态"""
        if self.current_state not in self.probability_dict:
            return self.current_state  # 终止状态，停在原地
        next_state = None
        probability_dict = self.probability_dict[self.current_state]
        cumulative_probability = 0.0
        random_value = random()
        for state in probability_dict:
            cumulative_probability += probability_dict[state]
            if random_value < cumulative_probability:
                next_state = state
                break
        return next_state

    def test_transfer_state(self):
        """测试 transfer_state 函数"""
        global n
        n = 0
        next_state = self.transfer_state()
        print(f"当前状态: {self.current_state}, 下一状态: {next_state}")
        self.current_state = next_state  # 更新当前状态
        n += 1
        return next_state  # 返回下一状态，以便测试



    def test_all(self):
        """测试所有函数"""
        self.test_transfer_state()
        self.validate_probability_dict()
        self.calibrate_probability_dict()
        self.simulate_process(rounds=1000)  # 测试 simulate_process 函数

    def simulate_process(self, rounds, verbose=True):
        """模拟系统运行指定轮数，输出每一步状态"""
        for i in range(rounds):
            next_state = self.transfer_state()
            if verbose:
                print(f"第 {i + 1} 步: 当前状态: {self.current_state}, 下一状态: {next_state}")
            self.current_state = next_state  # 更新 current_state 为 next_state


# 示例使用
if __name__ == '__main__':
    STATE_LIST = ["状态1", "状态2", "状态3"]
    PROBABILITY_DICT = {
        "状态1": {"状态1": 0.7, "状态2": 0.2, "状态3": 0.1},
        "状态2": {"状态1": 0.3, "状态2": 0.5, "状态3": 0.2},
        "状态3": {"状态1": 0.1, "状态2": 0.1, "状态3": 0.8}}

    simulator = MarkovChain(STATE_LIST, PROBABILITY_DICT)
    simulator.test_all()
