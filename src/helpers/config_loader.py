import yaml

def load_config(config_path: str = "config.yaml"):
    """YAML 설정 파일을 로드하는 함수"""
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"⚠️ 설정 파일을 불러오는 중 오류 발생: {e}")
        return {}
