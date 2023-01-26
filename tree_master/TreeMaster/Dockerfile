#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/runtime:6.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["TreeMaster/TreeMaster.csproj", "TreeMaster/"]
RUN dotnet restore "TreeMaster/TreeMaster.csproj"
COPY . .
WORKDIR "/src/TreeMaster"
RUN dotnet build "TreeMaster.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "TreeMaster.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

#EXPOSE 1337
EXPOSE 443

ENTRYPOINT ["dotnet", "TreeMaster.dll"]