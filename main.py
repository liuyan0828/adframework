
import pytest

if __name__ == '__main__':
    # s输出打印信息，v输出详细信息。不指定则运行所有
    pytest.main(['-v', '-s'])
    # 运行指定模块
    # pytest.main(['-vs', 'test_gphone.py'])
