FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS base
WORKDIR /app
EXPOSE 7106


# This stage is used to build the service project
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY ["FileVault.Server.csproj", "."]
RUN dotnet restore "./FileVault.Server.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "./FileVault.Server.csproj" -c Release -o /app/build

# This stage is used to publish the service project to be copied to the final stage
FROM build AS publish
RUN dotnet publish "./FileVault.Server.csproj" -c Release -o /app/publish /p:UseAppHost=false

# This stage is used in production or when running from VS in regular mode (Default when not using the Debug configuration)
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "FileVault.Server.dll"]