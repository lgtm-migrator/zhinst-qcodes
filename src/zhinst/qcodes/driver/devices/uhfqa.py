""" Autogenerated module for the UHFQA QCodes driver. """
from typing import List, Optional, Union, TypeVar
from zhinst.toolkit import CommandTable, Waveforms
from zhinst.qcodes.driver.devices.base import ZIBaseInstrument
from zhinst.qcodes.qcodes_adaptions import ZINode, ZIChannelList

Numpy2DArray = TypeVar("Numpy2DArray")


class QAS(ZINode):
    """Quantum Analyser Channel for the UHFQA.

    Args:
        root: Underlying node tree.
        tree: tree (node path as tuple) of the coresponding node.
    """

    def __init__(self, parent, tk_object, index, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self, parent, f"qas_{index}", snapshot_cache=snapshot_cache, zi_node=zi_node
        )
        self._tk_object = tk_object

    def crosstalk_matrix(self, matrix: Numpy2DArray = None) -> Optional[Numpy2DArray]:
        """Sets or gets the crosstalk matrix of the UHFQA as a 2D array.

        Args:
            matrix: The 2D matrix used in the digital signal
                processing path to compensate for crosstalk between the
                different channels. The given matrix can also be a part
                of the entire 10 x 10 matrix. Its maximum dimensions
                are 10 x 10 (default: None).

        Returns:
            If no argument is given the method returns the current
            crosstalk matrix as a 2D numpy array.

        Raises:
            ValueError: If the matrix size exceeds the maximum size of
                10 x 10

        """
        return self._tk_object.crosstalk_matrix(matrix=matrix)

    def adjusted_delay(self, value: int = None) -> int:
        """Set or get the adjustment in the quantum analyzer delay.

        Adjusts the delay that defines the time at which the integration starts
        in relation to the trigger signal of the weighted integration units.

        Depending if the deskew matrix is bypassed there exists a different
        default delay. This function can be used to add an additional delay to
        the default delay.

        Args:
            value: Number of additional samples to adjust the delay. If not
                specified this function will just return the additional delay
                currently set.

        Returns:
            The adjustment in delay in units of samples.

        Raises:
            ValueError: If the adjusted quantum analyzer delay is outside the
                allowed range of 1021 samples.

        """
        return self._tk_object.adjusted_delay(value=value)

class CommandTableNode(ZINode):
    """CommandTable node.

    This class implements the basic functionality of the command table allowing
    the user to load and upload their own command table.

    A dedicated class called ``CommandTable`` exists that is the prefered way
    to create a valid command table. For more information about the
    ``CommandTable`` refer to the corresponding example or the documentation
    of that class directly.

    Args:
        root: Node used for the upload of the command table
        tree: Tree (node path as tuple) of the current node
        device_type: Device type.
    """

    def __init__(self, parent, tk_object, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self,
            parent,
            f"commandtablenode",
            snapshot_cache=snapshot_cache,
            zi_node=zi_node,
        )
        self._tk_object = tk_object

    def check_status(self) -> bool:
        """Check status of the command table.

        Returns:
            Flag if a valid command table is loaded into the device.

        Raises:
            RuntimeError: If the command table upload into the device failed.
        """
        return self._tk_object.check_status()

    def load_validation_schema(self) -> dict:
        """Load device command table validation schema.

        Returns:
            JSON validation schema for the device command tables.
        """
        return self._tk_object.load_validation_schema()

    def upload_to_device(
        self, ct: Union[CommandTable, str, dict], *, validate: bool = True
    ) -> None:
        """Upload command table into the device.

        The command table can either be specified through the dedicated
        ``CommandTable`` class or in a raw format, meaning a json string or json
        dict. In the case of a json string or dict the command table is
        validated by default against the schema provided by the device.

        Args:
            ct: Command table.
            validate: Flag if the command table should be validated. (Only
                applies if the command table is passed as a raw json string or
                json dict)

        Raises:
            RuntimeError: If the command table upload into the device failed.
            zhinst.toolkit.exceptions.ValidationError: Incorrect schema.
        """
        return self._tk_object.upload_to_device(ct=ct, validate=validate)

    def load_from_device(self) -> CommandTable:
        """Load command table from the device.

        Returns:
            command table.
        """
        return self._tk_object.load_from_device()


class AWG(ZINode):
    """AWG node.

    This class implements the basic functionality for the device specific
    arbitrary waveform generator.
    Besides the upload/compilation of sequences it offers the upload of
    waveforms and command tables.

    Args:
        root: Root of the nodetree
        tree: Tree (node path as tuple) of the current node
        awg_module: Instance of the AWG Module
        daq_server: Instance of the ziDAQServer
        serial: Serial of the device.
        index: Index of the coresponding awg channel
        device_type: Device type
    """

    def __init__(self, parent, tk_object, index, snapshot_cache=None, zi_node=None):
        ZINode.__init__(
            self, parent, f"awg_{index}", snapshot_cache=snapshot_cache, zi_node=zi_node
        )
        self._tk_object = tk_object

        if self._tk_object.commandtable:

            self.add_submodule(
                "commandtable",
                CommandTableNode(
                    self,
                    self._tk_object.commandtable,
                    zi_node=self._tk_object.commandtable.node_info.path,
                    snapshot_cache=self._snapshot_cache,
                ),
            )

    def enable_sequencer(self, *, single: bool) -> None:
        """Starts the sequencer of a specific channel.

        Waits until the sequencer is enabled.

        Args:
            single: Flag if the sequencer should be disabled after finishing
            execution.
        """
        return self._tk_object.enable_sequencer(single=single)

    def wait_done(self, *, timeout: float = 10, sleep_time: float = 0.005) -> None:
        """Wait until the AWG is finished.

        Args:
            timeout: The maximum waiting time in seconds for the generator
                (default: 10).
            sleep_time: Time in seconds to wait between requesting generator
                state

        Raises:
            RuntimeError: If continuous mode is enabled
            TimeoutError: If the sequencer program did not finish within
                the specified timeout time
        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def load_sequencer_program(
        self, sequencer_program: str, *, timeout: float = 100.0
    ) -> None:
        """Compiles the current SequenceProgram on the AWG Core.

        Args:
            sequencer_program: Sequencer program to be uploaded
            timeout: Maximum time to wait for the compilation on the device in
                seconds.

        Raises:
            TimeoutError: If the upload or compilation times out.
            RuntimeError: If the upload or compilation failed.
        """
        return self._tk_object.load_sequencer_program(
            sequencer_program=sequencer_program, timeout=timeout
        )

    def write_to_waveform_memory(
        self, waveforms: Waveforms, indexes: list = None
    ) -> None:
        """Writes waveforms to the waveform memory.

        The waveforms must already be assigned in the sequencer programm.

        Args:
            waveforms: Waveforms that should be uploaded.

        Raises:
            IndexError: The index of a waveform exeeds the one on the device
            RuntimeError: One of the waveforms index points to a filler(placeholder)
        """
        return self._tk_object.write_to_waveform_memory(
            waveforms=waveforms, indexes=indexes
        )

    def read_from_waveform_memory(self, indexes: List[int] = None) -> Waveforms:
        """Read waveforms to the waveform memory.

        Args:
            indexes: List of waveform indexes to read from the device. If not
                specfied all assigned waveforms will be downloaded.

        Returns:
            Mutuable mapping of the downloaded waveforms.
        """
        return self._tk_object.read_from_waveform_memory(indexes=indexes)


class UHFQA(ZIBaseInstrument):
    """QCodes driver for the Zurich Instruments UHFQA."""

    def _init_additional_nodes(self):
        """init class specific modules and paramaters."""

        if self._tk_object.qas:

            channel_list = ZIChannelList(
                self,
                "qas",
                QAS,
                zi_node=self._tk_object.qas.node_info.path,
                snapshot_cache=self._snapshot_cache,
            )
            for i, x in enumerate(self._tk_object.qas):
                channel_list.append(
                    QAS(
                        self,
                        x,
                        i,
                        zi_node=self._tk_object.qas[i].node_info.path,
                        snapshot_cache=self._snapshot_cache,
                    )
                )
            # channel_list.lock()
            self.add_submodule("qas", channel_list)

        if self._tk_object.awgs:

            channel_list = ZIChannelList(
                self,
                "awgs",
                AWG,
                zi_node=self._tk_object.awgs.node_info.path,
                snapshot_cache=self._snapshot_cache,
            )
            for i, x in enumerate(self._tk_object.awgs):
                channel_list.append(
                    AWG(
                        self,
                        x,
                        i,
                        zi_node=self._tk_object.awgs[i].node_info.path,
                        snapshot_cache=self._snapshot_cache,
                    )
                )
            # channel_list.lock()
            self.add_submodule("awgs", channel_list)

    def enable_qccs_mode(self) -> None:
        """Configure the instrument to work with PQSC.

        This method sets the reference clock source and DIO settings
        correctly to connect the instrument to the PQSC.

        Info:
            Use ``factory_reset`` to reset the changes if necessary
        """
        return self._tk_object.enable_qccs_mode()