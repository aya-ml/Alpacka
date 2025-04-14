# robot_simulator.py
import cv2
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import threading
import time

class RobotSimulator:
    def __init__(self):
        self.sim_running = False
        self.current_frame = None
        self.thread = None
        self.client = None
        self.sim = None
        self.camera = None
        self.wheels = {}
        self.robot_handle = None
        self.square_movement_thread = None

    def connect(self):
        """Подключение к CoppeliaSim"""
        try:
            self.client = RemoteAPIClient()
            self.sim = self.client.require('sim')
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def initialize_robot(self):
        """Инициализация робота и его компонентов"""
        try:
            self.robot_handle = self.sim.getObject('/RobotnikSummitXL')
            
            self.wheels = {
                'front_left': self.sim.getObject('/RobotnikSummitXL/fl_joint/fl_respondable/front_left_wheel'),
                'front_right': self.sim.getObject('/RobotnikSummitXL/fr_joint/fr_respondable/front_right_wheel'),
                'back_left': self.sim.getObject('/RobotnikSummitXL/bl_joint/bl_respondable/back_left_wheel'),
                'back_right': self.sim.getObject('/RobotnikSummitXL/br_joint/br_respondable/back_right_wheel')
            }
            
            self.camera = self.sim.getObject('/RobotnikSummitXL/visionSensor')
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False

    def start_simulation(self):
        """Запуск симуляции в отдельном потоке"""
        if not self.sim_running:
            self.sim_running = True
            self.thread = threading.Thread(target=self._run_simulation, daemon=True)
            self.thread.start()
            
            # Запускаем движение по квадрату в отдельном потоке
            self.square_movement_thread = threading.Thread(
                target=self._run_square_movement, 
                daemon=True
            )
            self.square_movement_thread.start()

    def stop_simulation(self):
        """Остановка симуляции"""
        self.sim_running = False
        if self.thread:
            self.thread.join()
        if self.square_movement_thread:
            self.square_movement_thread.join()

    def _run_simulation(self):
        """Основной цикл симуляции"""
        self.sim.startSimulation()
        try:
            while self.sim_running:
                self._get_camera_image()
                time.sleep(0.05)
        finally:
            self.sim.stopSimulation()

    def _run_square_movement(self):
        """Движение робота по квадрату"""
        time.sleep(1)  # Даем симуляции время на запуск
        
        while self.sim_running:
            # Движение вперед (3 секунды)
            self.move(0.5, 0.5)
            start_time = time.time()
            while self.sim_running and time.time() - start_time < 3:
                time.sleep(0.1)
            
            if not self.sim_running:
                break
                
            # Поворот направо (1.5 секунды)
            self.move(0.5, -0.5)
            start_time = time.time()
            while self.sim_running and time.time() - start_time < 1.5:
                time.sleep(0.1)
            
            if not self.sim_running:
                break

    def move(self, left_speed, right_speed):
        """Управление движением робота"""
        if self.sim_running:
            self.sim.setJointTargetVelocity(self.wheels['front_left'], left_speed)
            self.sim.setJointTargetVelocity(self.wheels['front_right'], -right_speed)
            self.sim.setJointTargetVelocity(self.wheels['back_left'], left_speed)
            self.sim.setJointTargetVelocity(self.wheels['back_right'], -right_speed)

    def _get_camera_image(self):
        """Получение изображения с камеры"""
        try:
            img, res = self.sim.getVisionSensorImg(self.camera)
            self.current_frame = cv2.cvtColor(
                np.frombuffer(img, dtype=np.uint8).reshape(res[1], res[0], 3),
                cv2.COLOR_RGB2BGR
            )
        except:
            # Создаем черный кадр если не удалось получить изображение
            self.current_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def get_frame(self):
        """Получение текущего кадра для отображения"""
        if self.current_frame is None:
            # Первый кадр - черное изображение
            return np.zeros((480, 640, 3), dtype=np.uint8)
        return self.current_frame

    def is_running(self):
        """Проверка состояния симуляции"""
        return self.sim_running