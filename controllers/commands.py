def dashboard():
  response.veiw = 'commands/dashboard.html'
  return dict(forward=URL('receive',args=[],vars=dict(direction="forward")))

def receive():
  print(request.vars["direction"])
  return 'data'
