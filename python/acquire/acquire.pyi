from typing import (
    Any,
    ClassVar,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    final,
    overload,
)

from numpy.typing import NDArray

@final
class AvailableData:
    def frames(self) -> Iterator[VideoFrame]: ...
    def get_frame_count(self) -> int: ...
    def __iter__(self) -> Iterator[VideoFrame]: ...

@final
class AvailableDataContext:
    def __enter__(self) -> AvailableData: ...
    def __exit__(
        self, exc_type: Any, exc_value: Any, traceback: Any
    ) -> None: ...

@final
class Camera:
    identifier: Optional[DeviceIdentifier]
    settings: CameraProperties

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class CameraCapabilities:
    exposure_time_us: Property
    line_interval_us: Property
    readout_direction: Property
    binning: Property
    offset: OffsetCapabilities
    shape: ShapeCapabilities
    supported_pixel_types: List[SampleType]
    digital_lines: DigitalLineCapabilities
    triggers: TriggerCapabilities

    def dict(self) -> Dict[str, Any]: ...

@final
class CameraProperties:
    exposure_time_us: float
    line_interval_us: float
    binning: float
    pixel_type: SampleType
    readout_direction: Direction
    offset: Tuple[int, int]
    shape: Tuple[int, int]
    input_triggers: InputTriggers
    output_triggers: OutputTriggers

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class Capabilities:
    video: Tuple[VideoStreamCapabilities, VideoStreamCapabilities]

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class DeviceIdentifier:
    id: Tuple[int, int]
    kind: DeviceKind
    name: str

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...
    @staticmethod
    def none() -> DeviceIdentifier: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class DeviceKind:
    Camera: ClassVar[DeviceKind]
    NONE: ClassVar[DeviceKind]
    Signals: ClassVar[DeviceKind]
    StageAxis: ClassVar[DeviceKind]
    Storage: ClassVar[DeviceKind]

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class DeviceManager:
    def devices(self) -> List[DeviceIdentifier]: ...
    def select(
        self, kind: DeviceKind, name: Optional[str] = None
    ) -> Optional[DeviceIdentifier]: ...
    def select_one_of(
        self, kind: DeviceKind, names: List[str]
    ) -> Optional[DeviceIdentifier]: ...

@final
class DeviceState:
    Closed: ClassVar[DeviceState]
    AwaitingConfiguration: ClassVar[DeviceState]
    Armed: ClassVar[DeviceState]
    Running: ClassVar[DeviceState]

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class DigitalLineCapabilities:
    line_count: int
    names: Tuple[str, str, str, str, str, str, str, str]

    def dict(self) -> Dict[str, Any]: ...

@final
class DimensionType:
    """The storage dimension type.

    Space: spatial dimension.
    Channel: color channel dimension.
    Time: time dimension.
    Other: other dimension.

    When downsampling, Space and Time dimensions are downsampled by the same factor.
    Channel and Other dimensions are not downsampled.

    This value is also reflected in the dimension metadata of an OME-Zarr dataset.
    """

    Space: ClassVar[DimensionType]
    Channel: ClassVar[DimensionType]
    Time: ClassVar[DimensionType]
    Other: ClassVar[DimensionType]

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class Direction:
    Backward: ClassVar[Direction]
    Forward: ClassVar[Direction]

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class InputTriggers:
    acquisition_start: Trigger
    exposure: Trigger
    frame_start: Trigger

    def dict(self) -> Dict[str, Any]: ...

@final
class OffsetCapabilities:
    x: Property
    y: Property

    def dict(self) -> Dict[str, Any]: ...

@final
class OutputTriggers:
    exposure: Trigger
    frame_start: Trigger
    trigger_wait: Trigger

    def dict(self) -> Dict[str, Any]: ...

@final
class PID:
    derivative: float
    integral: float
    proportional: float

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class Properties:
    video: Tuple[VideoStream, VideoStream]

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class Property:
    writable: bool
    low: float
    high: float
    kind: PropertyType

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class PropertyType:
    FixedPrecision: ClassVar[PropertyType]
    FloatingPrecision: ClassVar[PropertyType]
    Enum: ClassVar[PropertyType]
    String: ClassVar[PropertyType]

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class Runtime:
    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def device_manager(self) -> DeviceManager: ...
    def get_available_data(self, stream_id: int) -> AvailableDataContext: ...
    def get_configuration(self) -> Properties: ...
    def get_capabilities(self) -> Capabilities: ...
    def get_state(self) -> DeviceState: ...
    def set_configuration(self, properties: Properties) -> Properties: ...
    def start(self) -> None: ...
    def execute_trigger(self, stream_id: int) -> None: ...
    def stop(self) -> None: ...
    def abort(self) -> None: ...

@final
class SampleRateHz:
    numerator: int
    denominator: int

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class SampleType:
    F32: ClassVar[SampleType]
    I16: ClassVar[SampleType]
    I8: ClassVar[SampleType]
    U16: ClassVar[SampleType]
    U8: ClassVar[SampleType]
    U10: ClassVar[SampleType]
    U12: ClassVar[SampleType]
    U14: ClassVar[SampleType]

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class ShapeCapabilities:
    x: Property
    y: Property

    def dict(self) -> Dict[str, Any]: ...

@final
class SignalIOKind:
    Input: ClassVar[SignalIOKind]
    Output: ClassVar[SignalIOKind]

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class SignalType:
    Analog: ClassVar[SignalType]
    Digital: ClassVar[SignalType]

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class Storage:
    identifier: Optional[DeviceIdentifier]
    settings: StorageProperties

    def dict(self) -> Dict[str, Any]: ...

@final
class StorageCapabilities:
    chunking_is_supported: bool
    sharding_is_supported: bool
    multiscale_is_supported: bool

    def dict(self) -> Dict[str, Any]: ...

@final
class StorageDimension:
    name: str
    kind: DimensionType
    array_size_px: int
    chunk_size_px: int
    shard_size_chunks: int

    def dict(self) -> Dict[str, Any]: ...

@final
class StorageProperties:
    external_metadata_json: Optional[str]
    filename: Optional[str]
    first_frame_id: int
    pixel_scale_um: Tuple[float, float]
    acquisition_dimensions: List[StorageDimension]
    enable_multiscale: bool

    def dict(self) -> Dict[str, Any]: ...

@final
class Trigger:
    edge: TriggerEdge
    enable: bool
    line: int
    kind: SignalIOKind

    def __init__(self, *args: None, **kwargs: Any) -> None: ...
    def dict(self) -> Dict[str, Any]: ...

@final
class TriggerCapabilities:
    acquisition_start: TriggerInputOutputCapabilities
    exposure: TriggerInputOutputCapabilities
    frame_start: TriggerInputOutputCapabilities

    def dict(self) -> Dict[str, Any]: ...

@final
class TriggerEdge:
    Falling: ClassVar[TriggerEdge]
    NotApplicable: ClassVar[TriggerEdge]
    Rising: ClassVar[TriggerEdge]
    AnyEdge: ClassVar[TriggerEdge]
    LevelLow: ClassVar[TriggerEdge]
    LevelHigh: ClassVar[TriggerEdge]

    def __eq__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __int__(self) -> int: ...
    def __le__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

@final
class TriggerInputOutputCapabilities:
    input: int
    output: int

    def dict(self) -> Dict[str, Any]: ...

@final
class VideoFrame:
    def data(self) -> NDArray[Any]: ...
    def metadata(self) -> VideoFrameMetadata: ...

@final
class VideoFrameMetadata:
    frame_id: int
    timestamps: VideoFrameTimestamps

    def dict(self) -> Dict[str, Any]: ...

@final
class VideoFrameTimestamps:
    hardware: int
    acq_thread: int

    def dict(self) -> Dict[str, Any]: ...

@final
class VideoStream:
    camera: Camera
    storage: Storage
    max_frame_count: int
    frame_average_count: int

    def dict(self) -> Dict[str, Any]: ...

@final
class VideoStreamCapabilities:
    camera: CameraCapabilities
    storage: StorageCapabilities
    max_frame_count: Property
    frame_average_count: Property

    def dict(self) -> Dict[str, Any]: ...

@final
class VoltageRange:
    mn: float
    mx: float

    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, mn: float, mx: float) -> None: ...
    def dict(self) -> Dict[str, float]: ...

def core_api_version() -> str: ...
