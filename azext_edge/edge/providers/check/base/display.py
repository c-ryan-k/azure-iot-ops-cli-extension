# coding=utf-8
# ----------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License file in the project root for license information.
# ----------------------------------------------------------------------------------------------

from itertools import groupby
from knack.log import get_logger
from rich.console import Console, NewLine
from rich.padding import Padding
from typing import Any, Dict, List, Optional, Tuple

from .check_manager import CheckManager
from ..common import ALL_NAMESPACES_TARGET, ResourceOutputDetailLevel
from ....common import CheckTaskStatus

logger = get_logger(__name__)


def add_display_and_eval(
    check_manager: CheckManager,
    target_name: str,
    display_text: str,
    eval_status: str,
    eval_value: str,
    resource_name: Optional[str] = None,
    namespace: str = ALL_NAMESPACES_TARGET,
    padding: Tuple[int, int, int, int] = (0, 0, 0, 8)
) -> None:
    check_manager.add_display(
        target_name=target_name,
        namespace=namespace,
        display=Padding(display_text, padding)
    )
    check_manager.add_target_eval(
        target_name=target_name,
        namespace=namespace,
        status=eval_status,
        value=eval_value,
        resource_name=resource_name
    )


class DisplayManager():
    def __init__(self, console: Console):
        self.console = console
        self.success_count = 0
        self.warning_count = 0
        self.error_count = 0
        self.skipped_count = 0

    def _increment_summary(self, status: str) -> None:
        if not status:
            return
        if status == CheckTaskStatus.success.value:
            self.success_count = self.success_count + 1
        elif status == CheckTaskStatus.warning.value:
            self.warning_count = self.warning_count + 1
        elif status == CheckTaskStatus.error.value:
            self.error_count = self.error_count + 1
        elif status == CheckTaskStatus.skipped.value:
            self.skipped_count = self.skipped_count + 1

    # TODO: test + refactor
    def display_as_list(self, result: Dict[str, Any], detail_level: int) -> None:

        def _print_summary() -> None:
            from rich.panel import Panel

            success_content = f"[green]{self.success_count} check(s) succeeded.[/green]"
            warning_content = f"{self.warning_count} check(s) raised warnings."
            warning_content = (
                f"[green]{warning_content}[/green]" if not self.warning_count else f"[yellow]{warning_content}[/yellow]"
            )
            error_content = f"{self.error_count} check(s) raised errors."
            error_content = f"[green]{error_content}[/green]" if not self.error_count else f"[red]{error_content}[/red]"
            skipped_content = f"[bright_white]{self.skipped_count} check(s) were skipped[/bright_white]."
            content = f"{success_content}\n{warning_content}\n{error_content}\n{skipped_content}"
            self.console.print(Panel(content, title="Check Summary", expand=False))

        title: dict = result.get("title")
        if title:
            self.console.print(NewLine(1))
            self.console.rule(title, align="center", style="blue bold")
            self.console.print(NewLine(1))

        pre_checks: List[dict] = result.get("preDeployment")
        if pre_checks:
            self.console.rule("Pre deployment checks", align="left")
            self.console.print(NewLine(1))
            self._enumerate_displays(pre_checks)

        post_checks: List[dict] = [check for check in result.get("postDeployment", []) if check]

        if detail_level == ResourceOutputDetailLevel.summary.value:
            self._summary_display(post_checks)
        elif post_checks:
            self.console.rule("Post deployment checks", align="left")
            self.console.print(NewLine(1))
            self._enumerate_displays(post_checks)

        _print_summary()

    def _enumerate_displays(self, checks: List[Dict[str, dict]]) -> None:
        for check in checks:
            status = check.get("status")
            prefix_emoji = _get_emoji_from_status(status)
            self.console.print(Padding(f"{prefix_emoji} {check['description']}", (0, 0, 0, 4)))

            targets = check.get("targets", {})
            for type in targets:
                for namespace in targets[type]:
                    namespace_target = targets[type][namespace]
                    displays = namespace_target.get("displays", [])
                    status = namespace_target.get("status")
                    for (idx, disp) in enumerate(displays):
                        # display status indicator on each 'namespaced' grouping of displays
                        if all([idx == 0, namespace != ALL_NAMESPACES_TARGET, status]):
                            prefix_emoji = _get_emoji_from_status(status)
                            self.console.print(Padding(f"\n{prefix_emoji} {disp.renderable}", (0, 0, 0, 6)))
                        else:
                            self.console.print(disp)
                    target_status = targets[type][namespace].get("status")
                    evaluations = targets[type][namespace].get("evaluations", [])
                    if not evaluations:
                        self._increment_summary(target_status)
                    for e in evaluations:
                        eval_status = e.get("status")
                        self._increment_summary(eval_status)
            self.console.print(NewLine(1))
        self.console.print(NewLine(1))

    def _summary_display(self, checks: List[Dict[str, dict]]) -> None:
        for check in checks:
            status = check.get("status")
            if not status or status == CheckTaskStatus.skipped.value:
                continue
            prefix_emoji = _get_emoji_from_status(status)
            self.console.print(Padding(f"{prefix_emoji} {check['description']}", (0, 0, 0, 4)))

            targets = check.get("targets", {})
            for _target in targets:  # diagnosticservices.mq.iotoperations.azure.com
                target = targets[_target]
                for _namespace in target:  # azure-iot-operations: {status,evaluation...}
                    namespace = target[_namespace]
                    namespace_suffix = '' if _namespace == ALL_NAMESPACES_TARGET else f" in {{[purple]{_namespace}[/purple]}}"
                    namespace_status = namespace.get("status")
                    if not namespace_status or namespace_status == CheckTaskStatus.skipped.value:
                        continue
                    target_emoji = _get_emoji_from_status(namespace_status)
                    self.console.print(Padding(f"- {target_emoji} {_target}{namespace_suffix}", (0, 0, 0, 8)))

                    # consolidate checks by resource name / type
                    def get_eval_display(eval: dict) -> Optional[str]:
                        return eval.get('name') or eval.get('summary')

                    evals = [eval for eval in namespace.get('evaluations', []) if get_eval_display(eval)]
                    if not evals:
                        self._increment_summary(namespace_status)
                    evals.sort(key=get_eval_display)
                    evals_by_resource = groupby(evals, key=get_eval_display)

                    for (eval_name, evals) in evals_by_resource:
                        evals = list(evals)
                        eval_desc = eval_name
                        # if more than one eval for a specific name,
                        if len(evals) > 1:
                            # determine worst_status for all evals
                            worst_status = CheckTaskStatus.success.value
                            for eval in evals:
                                eval_status = eval.get('status')
                                if eval_status == CheckTaskStatus.error.value:
                                    worst_status = CheckTaskStatus.error.value
                                elif eval_status == CheckTaskStatus.warning.value and worst_status != CheckTaskStatus.error.value:
                                    worst_status = CheckTaskStatus.warning.value
                            eval_status = worst_status
                            eval_emoji = _get_emoji_from_status(worst_status)
                        else:
                            eval = evals[0]
                            eval_status = eval.get('status')
                            eval_emoji = _get_emoji_from_status(eval_status)
                        self._increment_summary(eval_status)
                        self.console.print(Padding(f"- {eval_emoji} {eval_desc}", (0, 0, 0, 12)))
                self.console.print(NewLine(1))
        self.console.print(NewLine(1))


def _get_emoji_from_status(status: str) -> str:
    return "" if not status else CheckTaskStatus.map_to_colored_emoji(status)


def process_value_color(
    check_manager: CheckManager,
    target_name: str,
    key: Any,
    value: Any,
) -> str:
    value = value if value else "N/A"
    if "error" in str(key).lower() and str(value).lower() not in ["null", "n/a", "none", "noerror"]:
        check_manager.set_target_status(
            target_name=target_name,
            status=CheckTaskStatus.error.value
        )
        return f"[red]{value}[/red]"
    return f"[cyan]{value}[/cyan]"
