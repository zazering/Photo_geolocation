# tests/conftest.py - Конфигурация тестов
conftest_content = '''import pytest
import asyncio
from pathlib import Path
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import get_settings

settings = get_settings()

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(init_test_db) -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def override_get_db():
        return db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_image_path() -> Path:
    return Path(__file__).parent / "data" / "sample.jpg"


@pytest.fixture
def sample_image_bytes() -> bytes:
    return b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x02\\x00\\x00\\x00\\x90wS\\xde'
'''

with open("photo_geolocation/tests/conftest.py", "w") as f:
    f.write(conftest_content)

# tests/unit/test_image_processing.py
test_image_processing_content = '''import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from app.utils.image_processing import ImageProcessor


class TestImageProcessor:
    def setup_method(self):
        self.processor = ImageProcessor()
    
    def test_validate_image_file_not_exists(self):
        result, error = self.processor.validate_image(Path("nonexistent.jpg"))
        assert result is False
        assert "does not exist" in error
    
    @patch('app.utils.image_processing.Image.open')
    def test_validate_image_success(self, mock_open):
        mock_img = Mock()
        mock_img.format = "JPEG"
        mock_open.return_value.__enter__.return_value = mock_img
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_size = 1000
                
                result, error = self.processor.validate_image(Path("test.jpg"))
                assert result is True
                assert error is None
    
    def test_generate_hash(self):
        with patch('builtins.open', mock_open(read_data=b"test data")):
            hash_result = self.processor.generate_hash(Path("test.jpg"))
            assert len(hash_result) == 64
    
    def test_extract_metadata_basic(self):
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                mock_stat.return_value.st_size = 1000
                
                with patch('app.utils.image_processing.Image.open') as mock_open:
                    mock_img = Mock()
                    mock_img.format = "JPEG"
                    mock_img.width = 1920
                    mock_img.height = 1080
                    mock_open.return_value.__enter__.return_value = mock_img
                    
                    metadata = self.processor.extract_metadata(Path("test.jpg"))
                    
                    assert metadata["format"] == "JPEG"
                    assert metadata["dimensions"]["width"] == 1920
                    assert metadata["dimensions"]["height"] == 1080
    
    def test_convert_to_degrees(self):
        value = [40, 45, 30]
        result = self.processor._convert_to_degrees(value)
        expected = 40 + 45/60.0 + 30/3600.0
        assert abs(result - expected) < 0.0001


def mock_open(read_data=b""):
    from unittest.mock import mock_open as original_mock_open
    return original_mock_open(read_data=read_data)
'''

with open("photo_geolocation/tests/unit/test_image_processing.py", "w") as f:
    f.write(test_image_processing_content)

print("✅ Тесты созданы")