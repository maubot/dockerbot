# dockerbot - A maubot plugin to manage Docker containers.
# Copyright (C) 2020 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional

from aiodocker import Docker
from aiodocker.containers import DockerContainer
from aiodocker.exceptions import DockerError

from maubot import Plugin, MessageEvent
from maubot.handlers import command


def optional_int(val: str) -> Optional[int]:
    if not val:
        return None
    return int(val)


class DockerBot(Plugin):
    docker: Docker

    async def start(self) -> None:
        self.docker = Docker()

    @command.new("docker", require_subcommand=True)
    async def cmd(self) -> None:
        pass

    @staticmethod
    def _format_container(container: DockerContainer) -> str:
        name = container["Names"][0][1:]
        id = container["Id"][:12]
        state = container["State"]
        return f"* `{id}`: {name} ({state})"

    @cmd.subcommand("ps")
    async def ps(self, evt: MessageEvent) -> None:
        containers = await self.docker.containers.list(all=True)
        if not containers:
            await evt.reply("No containers :(")
            return
        await evt.reply("\n".join(self._format_container(cont) for cont in containers))

    @cmd.subcommand("restart")
    @command.argument("name", label="container name")
    @command.argument("timeout", parser=optional_int, required=False)
    async def restart(self, evt: MessageEvent, name: str, timeout: Optional[int] = None) -> None:
        containers = await self.docker.containers.list(all=True)
        name = f"/{name}"
        container = None
        for container in containers:
            if name in container["Names"]:
                break
        if not container:
            await evt.reply("No container with that name found")
            return
        try:
            await container.restart(timeout)
            await evt.reply("Container restarted successfully")
        except DockerError:
            await evt.reply("Failed to restart container")
