import time
import gym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor

class MyQTable():
    def __init__(self, num_action):         # QTableをファイルから取得
        Qvalue_path = 'Qvalue.txt'
        
        # self._Qtable = np.random.uniform(low=-1, high=1, size=(num_digitized**4, num_action))
        self._Qtable = np.loadtxt(Qvalue_path)

    def get_action(self, next_state, epsilon):
        if epsilon > np.random.uniform(0, 1):
            next_action = np.random.choice([0, 1])
        else:
            a = np.where(self._Qtable[next_state]==self._Qtable[next_state].max())[0]
            next_action = np.random.choice(a)
        return next_action

    def update_Qtable(self, state, action, reward, next_state):
        alpha = 0.2
        gamma = 0.99
        next_maxQ = max(self._Qtable[next_state])
        self._Qtable[state, action] = (1 - alpha) * self._Qtable[state, action] + alpha * (reward + gamma * next_maxQ)

        return self._Qtable

num_digitized = 6

def digitized_state(observation):
    p, v, a, w = observation
    d = num_digitized
    pn = np.digitize(p, np.linspace(-2.4, 2.4, d+1)[1:-1])
    vn = np.digitize(v, np.linspace(-3.0, 3.0, d+1)[1:-1])
    an = np.digitize(a, np.linspace(-0.5, 0.5, d+1)[1:-1])
    wn = np.digitize(w, np.linspace(-2.0, 2.0, d+1)[1:-1])

    return pn + vn*d + an*d**2 + wn*d**3

def main():
    step_list = []
    frames = []                     # 画像保存用変数
    num_episodes = 1000             # 最大エピソード数
    max_number_of_steps = 200       # 1エピソード当たりのステップ数
    complete_episode = 0            # 完了エピソード数
    is_final_episode = False        # 最終判定フラグ
    save_path = ''            # 動画像保存先ディレクトリ
    
    env = gym.make('CartPole-v1', render_mode = 'rgb_array')
    tab = MyQTable(env.action_space.n)
    for episode in range(num_episodes):
        observation, _= env.reset()
        state = digitized_state(observation)
        episode_reward = 0
            
        for t in range(max_number_of_steps):

            if is_final_episode:
                frames.append(env.render())

            epsilon = 0.5*(1/(episode + 1))
            action = tab.get_action(state, epsilon)
            observation, reward, terminated, truncated, _ = env.step(action)
            done = truncated or terminated
            
            if done:
                if t < max_number_of_steps - 1:
                    reward -= max_number_of_steps
                    complete_episode = 0
                else:
                    reward += 1
                    # complete_episode += 1
                    print(f'CE{complete_episode}')
                    break

            next_state = digitized_state(observation)
            q_table = tab.update_Qtable(state, action, reward, next_state)
            state = next_state
            episode_reward += reward

            if done:
                step_list.append(t + 1)
                break
        
        # 結果をpngとmp4で出力
        if is_final_episode:
            print(f'結果を書き出します　[保存先] {save_path}')
            es = np.arange(0, len(step_list))
            plt.plot(es, step_list)
            plt.savefig("CartPoleReward.png")
            print(f'png書き出し完了')
            
            plt.figure()
            patch = plt.imshow(frames[0])
            plt.axis('off')

            def animate(i):
                patch.set_data(frames[i])

            anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(frames), interval=50)
            anim.save('CartPoleMovie.mp4', "ffmpeg")
            print(f'mp4書き出し完了')
            break
        
        # 100エピソード連続完了で最終試行へ
        if episode_reward == 200:
            complete_episode += 1
        else:
            complete_episode = 0

        if complete_episode >= 100:
            print('100回連続成功')
            is_final_episode = True

        print(f'Episode:{episode:4.0f}, R:{episode_reward:4.0f}')
    
    # 最終的なQTableをファイルに出力
    np.savetxt('Qvalue.txt', q_table)

def func():
    time.sleep(1)

def run():
    print("------normal------")
    start = time.time()
    main()
    print(f"処理時間：{time.time() - start}")
    
    print("------multithread------")
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as exec:
        exec.submit(main)
    print(f"処理時間：{time.time() - start}")

    print("------multiprocess------")
    start = time.time()
    with ProcessPoolExecutor(max_workers=5) as exec:
        exec.submit(main)
    print(f"処理時間：{time.time() - start}")

    
    
if __name__ == '__main__':
    run()