"""Autogenerated module for the BaseModule QCoDeS driver."""
import typing as t
from zhinst.qcodes.driver.devices.base import ZIBaseInstrument
from zhinst.toolkit.driver.modules import ModuleType as TKModuleType
from zhinst.toolkit.driver.modules.base_module import BaseModule as TKBaseModule
from zhinst.toolkit.driver.modules.base_module import ZIModule
from zhinst.toolkit.nodetree import Node as TKNode

from zhinst.qcodes.qcodes_adaptions import (
    ZIParameter,
    ZIInstrument,
    init_nodetree,
    tk_node_to_parameter,
)

if t.TYPE_CHECKING:
    from zhinst.qcodes.session import Session


class ZIBaseModule(ZIInstrument):
    """Generic toolkit driver for a LabOne Modules.

    All module specific class are derived from this class.
    It exposes the nodetree and also implements common functions valid for all
    modules.
    It also can be used directly, e.g. for modules that have no special class
    in toolkit.


    Args:
        tk_object: Underlying zhinst-toolkit object.
        session: Session to the Data Server.
        name: Name of the module in QCoDeS.
    """

    def __init__(self, tk_object: TKModuleType, session: "Session", name: str):
        self._tk_object = tk_object
        self._session = session
        super().__init__(
            f"zi_{name}_{len(self.instances())}", tk_object.root, is_module=True
        )
        init_nodetree(self, self._tk_object, self._snapshot_cache)

        self._tk_object.root.update_nodes(
            {
                "/device": {
                    "GetParser": lambda value: self._get_device(value),
                }
            },
            raise_for_invalid_node=False,
        )

    def _get_device(self, serial: str) -> t.Union[t.Type[ZIBaseInstrument], str]:
        """Convert a device serial into a QCoDeS device object.

        Args:
            serial: Serial of the device

        Returns:
            QCoDeS device object. If the serial does not
                match to a connected device the serial is returned instead.
        """
        try:
            return self._session.devices[serial]
        except (RuntimeError, KeyError):
            return serial

    def _get_node(self, node: str) -> t.Union[ZIParameter, str]:
        """Convert a raw node string into a qcodes node.

        Args:
            node (str): raw node string

        Returns:
            Node: qcodes node. (if the node can not be converted the raw node
                string is returned)
        """
        tk_node = self._tk_object._get_node(node)
        if isinstance(tk_node, str):
            return tk_node
        device = self._session.devices[tk_node.root.prefix_hide]
        return tk_node_to_parameter(device, tk_node)

    @staticmethod
    def _set_node(signal: t.Union[ZIParameter, TKNode, str]) -> str:
        """Convert a toolkit node into a raw node string.

        Args:
            signal (Union[Node,str]): node

        Returns:
            str: raw string node
        """
        try:
            node = signal.zi_node  # type: ignore[union-attr]
        except AttributeError:
            node = TKBaseModule._set_node(signal)
        return node

    def subscribe(self, signal: t.Union[ZIParameter, str]):
        """Subscribe to a node.

        The node can either be a node of this module or of a connected device.

        Args:
            signal (Node): node that should be subscribed.
        """
        try:
            self._tk_object.subscribe(signal.zi_node)  # type: ignore[union-attr]
        except AttributeError:
            self._tk_object.subscribe(signal)

    def unsubscribe(self, signal: t.Union[ZIParameter, str]):
        """Unsubscribe from a node.

        The node can either be a node of this module or of a connected device.

        Args:
            signal (Node): node that should be unsubscribe.
        """
        try:
            self._tk_object.unsubscribe(signal.zi_node)  # type: ignore[union-attr]
        except AttributeError:
            self._tk_object.unsubscribe(signal)

    @property
    def raw_module(self) -> ZIModule:  # type: ignore [type-var]
        """Underlying zhinst.core module."""
        return self._tk_object.raw_module

    def wait_done(self, *, timeout: float = 20.0, sleep_time: float = 0.5) -> None:
        """Waits until the module is finished.

        Warning: Only usable for modules that make use of the `/finished` node.

        Args:
            timeout (float): The maximum waiting time in seconds for the
                measurement (default: 20).
            sleep_time (int): Time in seconds to wait between
                requesting sweeper state. (default: 0.5)

        Raises:
            TimeoutError: The measurement is not completed before
                timeout.
        """
        return self._tk_object.wait_done(timeout=timeout, sleep_time=sleep_time)

    def execute(self) -> None:
        """Start the module execution.

        Subscription or unsubscription is not possible until the execution is
        finished.

        .. versionadded:: 0.4.1
        """
        return self._tk_object.execute()
